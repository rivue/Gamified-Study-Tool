<template>
    <div>
      <div v-if="loading" id="loadingCloud" class="cloud-animation">☁️</div>
      <div id="graph"></div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, onMounted } from "vue";
  import { useRouter } from "vue-router";
  import axios from "axios";
  import * as d3 from "d3";
  
  // Define interfaces for your data
  interface NodeData {
    name: string;
    category: string;
    x: number;
    y: number;
    id?: string;
    domRef?: HTMLElement;
  }
  
  interface LinkData {
    source: number;
    target: number;
    value: number;
  }
  
  interface GraphData {
    nodes: NodeData[];
    links: LinkData[];
    edges?: any; // if you need to keep the raw 'edges'
  }
  
  // Reactive state
  const loading = ref(true);
  const graphData = reactive<GraphData>({
    nodes: [],
    links: [],
  });
  const selectedNode = ref<NodeData | null>(null);
  const showingSuggestions = ref(false);
  
  // D3-related refs
  const svg = ref<d3.Selection<SVGSVGElement, unknown, HTMLElement, any> | null>(null);
  const graphGroup = ref<d3.Selection<SVGGElement, unknown, HTMLElement, any> | null>(null);
  const simulation = ref<any>(null); // Use 'any' or a proper d3.Simulation type when possible
  const zoom = ref<d3.ZoomBehavior<Element, unknown> | null>(null);
  
  // Other state variables
  const width = ref<number>(0);
  const height = ref<number>(0);
  const currentZoomScale = ref<number>(1);
  const baseCollisionRadius = 70;
  
  // Access router to perform routing actions
  const router = useRouter();
  
  //
  // Methods (converted to top-level functions)
  //
  
  function fetchGraphData(): Promise<void> {
    return axios
      .get("/api/knowledge-net")
      .then((response) => {
        // Assuming your API returns { data: { nodes: [...], edges: [...] } }
        Object.assign(graphData, response.data.data);
        // Convert edges to D3 links format:
        graphData.links = (graphData.edges || []).map((edge: any) => ({
          source: graphData.nodes.findIndex((node) => node.name === edge.from),
          target: graphData.nodes.findIndex((node) => node.name === edge.to),
          value: edge.similarity,
        }));
        loading.value = false;
        // Optionally, if a nodeName was provided via query params, select that node
        const nodeName = router.currentRoute.value.query.node as string | undefined;
        renderGraph(nodeName);
      })
      .catch((error) => {
        console.error("Error fetching graph data:", error);
        loading.value = false;
      });
  }
  
  function renderGraph(nodeName?: string) {
    // Set dimensions
    width.value = window.innerWidth - 42;
    height.value = window.innerHeight - 250;
  
    svg.value = d3
      .select("#graph")
      .append("svg")
      .attr("width", width.value)
      .attr("height", height.value);
  
    graphGroup.value = svg.value.append("g");
  
    simulation.value = d3
      .forceSimulation(graphData.nodes)
      .force(
        "link",
        d3
          .forceLink(graphData.links)
          .id((d: any) => d.index)
          .strength((d: any) => d.value)
      )
      .force("charge", d3.forceManyBody().strength(-30))
      .force("collide", d3.forceCollide(baseCollisionRadius))
      .force("center", d3.forceCenter(width.value / 2, height.value / 2));
  
    const linkColor = getComputedStyle(document.documentElement)
      .getPropertyValue("--element-color-1")
      .trim();
  
    // Draw Links
    const linkSelection = graphGroup.value
      .append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(graphData.links)
      .enter()
      .append("line")
      .attr("stroke", linkColor)
      .attr("stroke-width", (d: LinkData) => 5 * Math.sqrt(d.value));
  
    // Draw Nodes
    const nodeSelection = graphGroup.value
      .append("g")
      .attr("class", "nodes")
      .selectAll("foreignObject")
      .data(graphData.nodes, (d: NodeData) => d.name)
      .enter()
      .append("foreignObject")
      .attr("width", 280)
      .attr("height", 1)
      .each(function (d: NodeData) {
        const fo = d3.select(this);
        fo.append("xhtml:button")
          .attr("class", "content-button")
          .classed("completed-button", (node: NodeData) =>
            node.category.includes("completed")
          )
          .html((node: NodeData) => {
            const emoji = getEmojiForContentType(node.category);
            const contentName = removeEmoji(node.name);
            const extractedEmoji = extractEmoji(node.name);
            return `
              ${emoji ? `<span class="emoji-indicator">${emoji}</span>` : ""}
              <span class="content-name">${contentName}</span>
              ${
                extractedEmoji
                  ? `<span class="emoji-indicator">${extractedEmoji}</span>`
                  : ""
              }
            `;
          });
        // After render, set dimensions based on the button size
        setTimeout(() => {
          const buttonEl = this.querySelector("button.content-button") as HTMLElement;
          if (buttonEl) {
            const rect = buttonEl.getBoundingClientRect();
            d3.select(this).attr("width", rect.width).attr("height", rect.height);
          }
        }, 0);
      })
      .on("click", (event: MouseEvent, d: NodeData) => {
        selectNode(d);
      })
      .call(
        d3.drag<any, NodeData>()
          .on("start", (event: any, d: NodeData) => {
            if (!event.active) simulation.value.alphaTarget(0.2).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event: any, d: NodeData) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event: any, d: NodeData) => {
            if (!event.active) simulation.value.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );
    // Save node selection for future updates
    // (In a real app you’d store these in refs or reactive state)
    // Setup zoom behavior
    zoom.value = d3.zoom().on("zoom", (event) => {
      currentZoomScale.value = event.transform.k;
      graphGroup.value?.attr("transform", event.transform);
      simulation.value.force("collide", d3.forceCollide(baseCollisionRadius * currentZoomScale.value));
      simulation.value.alpha(0.02).restart();
    });
    svg.value.call(zoom.value);
  
    simulation.value.on("tick", () => {
      // Update links positions
      linkSelection
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);
      // Update node positions (adjust as needed)
      nodeSelection.attr("x", (d: any) => d.x - 110).attr("y", (d: any) => d.y - 30);
    });
  
    // If a nodeName was provided, select that node after rendering
    if (nodeName) {
      const nodeToSelect = graphData.nodes.find((n) => n.name === nodeName);
      if (nodeToSelect) {
        setTimeout(() => {
          selectNode(nodeToSelect);
        }, 1200);
      }
    }
  
    simulation.value.alpha(1).restart();
    setTimeout(() => {
      simulation.value.stop();
    }, 1200);
  }
  
  function selectNode(nodeData: NodeData) {
    deselectNode();
  
    if (selectedNode.value === nodeData) {
      selectedNode.value = null;
    } else {
      selectedNode.value = nodeData;
    }
  
    // Find and attach the DOM reference for the node
    const allNodes = d3.selectAll(".content-button").nodes();
    nodeData.domRef = allNodes.find(
      (el) => d3.select(el).datum() === nodeData
    ) as HTMLElement | undefined;
  
    if (selectedNode.value && nodeData.domRef) {
      d3.select(nodeData.domRef).classed("selected", true);
  
      // Center and zoom into the selected node
      const zoomLevel = 1.4;
      const translateX = width.value / 2 - nodeData.x * zoomLevel;
      const translateY = height.value / 2 - nodeData.y * zoomLevel;
      svg.value
        ?.transition()
        .duration(1000)
        .call(zoom.value!.transform, d3.zoomIdentity.translate(translateX, translateY).scale(zoomLevel));
  
      createActionButtons(nodeData);
    }
  }
  
  function deselectNode() {
    d3.select("#graph svg").selectAll(".node-buttons").remove();
    showingSuggestions.value = false;
    if (selectedNode.value && selectedNode.value.domRef) {
      d3.select(selectedNode.value.domRef).classed("selected", false);
    }
    selectedNode.value = null;
  }
  
  // Dummy functions for emojis—you should replace these with your own logic.
  function getEmojiForContentType(contentType: string): string {
    switch (contentType) {
      case "lesson":
      case "completed_lesson":
        return "📖";
      case "library":
      case "completed_librarie":
        return "🏛️";
      default:
        return "☁️";
    }
  }
  
  function extractEmoji(content: string): string {
    const emojiRegex =
      /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;
    const match = content.match(emojiRegex);
    return match ? match[0] : "";
  }
  
  function removeEmoji(content: string): string {
    const emoji = extractEmoji(content);
    return content.replace(emoji, "").trim();
  }
  
  // For the action buttons at the bottom of a node
  function createActionButtons(nodeData: NodeData): void {
    const canvasSize = { width: width.value, height: height.value };
    const buttonSize = { width: 120, height: 30 };
  
    const buttonGroup = d3
      .select("#graph svg")
      .append("g")
      .classed("node-buttons", true)
      .attr("transform", `translate(0, ${canvasSize.height - buttonSize.height - 20})`);
  
    if (nodeData.category === "offered_lesson") {
      // Library Button
      buttonGroup
        .append("foreignObject")
        .attr("width", buttonSize.width)
        .attr("height", buttonSize.height + 16)
        .attr("x", canvasSize.width / 2 - buttonSize.width - 16)
        .attr("y", 0)
        .append("xhtml:div")
        .attr("class", "knowledge-menu-button goto-button")
        .text("🏛️Library")
        .on("click", () => handleSuggestionLibrary(nodeData.name));
  
      // Lesson Button
      buttonGroup
        .append("foreignObject")
        .attr("width", buttonSize.width)
        .attr("height", buttonSize.height + 16)
        .attr("x", canvasSize.width / 2 + 16)
        .attr("y", 0)
        .append("xhtml:div")
        .attr("class", "knowledge-menu-button explore-button")
        .text("📖Lesson")
        .on("click", () => handleSuggestionLesson(nodeData.name));
    } else {
      // "Go to" Button
      buttonGroup
        .append("foreignObject")
        .attr("width", buttonSize.width)
        .attr("height", buttonSize.height + 16)
        .attr("x", canvasSize.width / 2 + 16)
        .attr("y", 0)
        .append("xhtml:div")
        .attr("class", "knowledge-menu-button goto-button")
        .text("📖Go to")
        .on("click", () => goToNode(nodeData));
  
      // "Explore" Button
      buttonGroup
        .append("foreignObject")
        .attr("width", buttonSize.width)
        .attr("height", buttonSize.height + 16)
        .attr("x", canvasSize.width / 2 - buttonSize.width - 16)
        .attr("y", 0)
        .append("xhtml:div")
        .attr("class", "knowledge-menu-button explore-button")
        .text("🔍Explore")
        .on("click", () => exploreNode(nodeData));
    }
  }
  
  function goToNode(nodeData: NodeData): void {
    let path: string | undefined;
    if (nodeData.category.includes("lesson")) {
      path = `/lesson/${nodeData.id}`;
    } else if (nodeData.category.includes("librar")) {
      path = `/create/${nodeData.id}`;
    }
    if (path) {
      router.push(path);
    }
  }
  
  async function exploreNode(nodeData: NodeData) {
    if (showingSuggestions.value) {
      removeSuggestionNodes();
      showingSuggestions.value = false;
      updateExploreButtonText("🔍Explore");
    } else {
      updateExploreButtonText("⏳Loading");
      try {
        const response = await fetch(`/api/explore?name=${nodeData.name}`);
        const data = await response.json();
        if (data && data.suggestions) {
          addSuggestionsToGraph(data.suggestions, nodeData);
          showingSuggestions.value = true;
          updateExploreButtonText("🔽Hide");
        } else {
          updateExploreButtonText("🔍Explore");
        }
      } catch (error) {
        console.error("Error exploring node:", error);
        updateExploreButtonText("🔍Explore");
      }
    }
  }
  
  function updateExploreButtonText(newText: string): void {
    d3.select("#graph svg").select(".explore-button").text(newText);
  }
  
  function updateGoToButtonText(newText: string): void {
    d3.select("#graph svg").select(".goto-button").text(newText);
  }
  
  function addSuggestionsToGraph(suggestions: string[], nodeData: NodeData): void {
    const originIndex = graphData.nodes.indexOf(nodeData);
    suggestions.forEach((suggestion) => {
      const newNode: NodeData = { name: suggestion, category: "suggestion", x: nodeData.x, y: nodeData.y };
      graphData.nodes.push(newNode);
      const newNodeIndex = graphData.nodes.length - 1;
      graphData.links.push({ source: originIndex, target: newNodeIndex, value: 0.1 });
    });
    updateGraph();
    simulation.value.alpha(0.1).restart();
  }
  
  function removeSuggestionNodes(): void {
    const suggestionNodes = graphData.nodes.filter((n) => n.category === "suggestion");
    if (suggestionNodes.length > 0) {
      const suggestionIndices = new Set(suggestionNodes.map((n) => graphData.nodes.indexOf(n)));
      graphData.nodes = graphData.nodes.filter((n, i) => !suggestionIndices.has(i));
      graphData.links = graphData.links.filter(
        (l: any) =>
          !suggestionIndices.has((l.source as any).index) &&
          !suggestionIndices.has((l.target as any).index)
      );
      updateGraph();
      simulation.value.alpha(0.1).restart();
    }
    showingSuggestions.value = false;
    d3.select("#graph svg").selectAll(".node-buttons").remove();
    if (selectedNode.value && selectedNode.value.domRef) {
      d3.select(selectedNode.value.domRef).classed("selected", false);
    }
    selectedNode.value = null;
  }
  
  function updateGraph(): void {
    const linkColor = getComputedStyle(document.documentElement)
      .getPropertyValue("--element-color-1")
      .trim();
    // Update links
    let linkSelection = graphGroup.value!
      .select(".links")
      .selectAll("line")
      .data(graphData.links, (d: any) => `${(d.source as any).index}-${(d.target as any).index}`);
    linkSelection.exit().remove();
    linkSelection = linkSelection
      .enter()
      .append("line")
      .attr("stroke", linkColor)
      .attr("stroke-width", (d: any) => 5 * Math.sqrt(d.value))
      .merge(linkSelection);
    // Update nodes
    const nodeGroup = graphGroup.value!
      .select(".nodes")
      .selectAll("foreignObject")
      .data(graphData.nodes, (d: NodeData) => d.name);
    nodeGroup.exit().remove();
    const nodeEnter = nodeGroup
      .enter()
      .append("foreignObject")
      .attr("width", 1)
      .attr("height", 1)
      .each(function (d: NodeData) {
        const fo = d3.select(this);
        fo.append("xhtml:button")
          .attr("class", "content-button")
          .classed("completed-button", (node: NodeData) => node.category.includes("completed"))
          .html((node: NodeData) => {
            const emoji = getEmojiForContentType(node.category);
            const contentName = removeEmoji(node.name);
            const extractedEmoji = extractEmoji(node.name);
            return `
                ${emoji ? `<span class="emoji-indicator">${emoji}</span>` : ""}
                <span class="content-name">${contentName}</span>
                ${
                  extractedEmoji
                    ? `<span class="emoji-indicator">${extractedEmoji}</span>`
                    : ""
                }
              `;
          });
        setTimeout(() => {
          const buttonEl = (this as HTMLElement).querySelector("button.content-button") as HTMLElement;
          if (buttonEl) {
            const rect = buttonEl.getBoundingClientRect();
            d3.select(this).attr("width", rect.width).attr("height", rect.height);
          }
        }, 0);
      })
      .on("click", (event: MouseEvent, d: NodeData) => {
        selectNode(d);
      })
      .call(
        d3
          .drag<any, NodeData>()
          .on("start", (event: any, d: NodeData) => {
            if (!event.active) simulation.value.alphaTarget(0.2).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event: any, d: NodeData) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event: any, d: NodeData) => {
            if (!event.active) simulation.value.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );
    node.value = nodeEnter.merge(nodeGroup);
    simulation.value.nodes(graphData.nodes);
    simulation.value.force("link").links(graphData.links);
  }
    
  onMounted(() => {
    fetchGraphData();
  });
  </script>
  
  <style>
  
.knowledge-menu-button {
  text-align: center;
  margin: 0px;
  padding: 8px 16px;
  background-color: var(--background-color-1t);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  cursor: pointer;
  display: inline-block;
  transition: transform 0.1s, background-color 0.1s;
}

.knowledge-menu-button:hover {
  background-color: var(--element-color-1);
}

.content-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background: var(--element-color-1);
  border: 2px solid var(--background-color-1t);
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  position: relative;
  transition: all 0.3s ease;
}

.selected {
  border-color: var(--highlight-color);
}

.content-name {
  padding: 8px;
}

.content-button .emoji-indicator {
  font-size: 1.5rem;
}

.content-button:hover {
  border-color: var(--element-color-2);
}

.completed-button {
  border-color: var(--gold-color);
  opacity: 0.9;
  position: relative;
}

.completed-button::after {
  content: "✓";
  color: #50c878;
  font-weight: bold;
  font-size: 1.2rem;
  position: absolute;
  right: 10px;
  top: 80%;
  transform: translateY(-50%);
}

.cloud-animation {
  font-size: 3em;
  position: absolute;
  top: 40%;
  left: 50%;
  animation: cloudMove 3s linear infinite;
}

@keyframes cloudMove {
  0% {
    opacity: 0;
    transform: translateX(-25vw) translateY(-2vh);
  }
  25% {
    transform: translateX(-12.5vw) translateY(2vh);
  }
  50% {
    opacity: 1;
    transform: translateX(0vw) translateY(-2vh);
  }
  75% {
    transform: translateX(12.5vw) translateY(2vh);
  }
  100% {
    opacity: 0;
    transform: translateX(25vw) translateY(-2vh);
  }
}
</style>
