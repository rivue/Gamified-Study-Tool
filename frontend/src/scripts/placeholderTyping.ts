import { ref, onMounted, onUnmounted } from 'vue';

export function useTypingEffect(elem: HTMLInputElement, topics: string[]) {
    const currentIndex = ref(0);
    const isDeleting = ref(false);
    const text = ref('');
    const typingSpeed = ref(75);
    let timer: number | null = null;

    function type() {
        const currentTopic = topics[currentIndex.value];
        const fullText = currentTopic;

        text.value = isDeleting.value
            ? fullText.substring(0, text.value.length - 1)
            : fullText.substring(0, text.value.length + 1);

        elem.placeholder = text.value;

        let typeSpeed = typingSpeed.value;

        if (isDeleting.value) {
            typeSpeed /= 4;
        }

        if (!isDeleting.value && text.value === fullText) {
            typeSpeed = 1500;
            isDeleting.value = true;
        } else if (isDeleting.value && text.value === '') {
            isDeleting.value = false;
            typeSpeed = 500;
            currentIndex.value = (currentIndex.value + (Math.floor(Math.random() * topics.length))) % topics.length;
        }

        clearTimeout(timer as number);
        timer = setTimeout(type, typeSpeed) as unknown as number;
    }

    const start = () => {
        type();
    };

    const stop = () => {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
    };

    onUnmounted(() => {
        stop();
    });

    return {
        start,
        stop
    };
}
