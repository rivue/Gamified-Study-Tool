const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  devServer: { // I (Will Gunter) added
    webSocketServer: false,
  },
  transpileDependencies: true,
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: 'Rivue.ai | Learn anything'
    }
  },
});
