const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  devServer: {
    webSocketServer: false,
  },
  transpileDependencies: true,
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: 'Rivue.ai | Learn anything',
    },
  },
  configureWebpack: {
    resolve: {
      extensions: ['.ts', '.js', '.vue', '.json'],
    },
  },
  chainWebpack: (config) => {
    // Fix the ESLint plugin passing invalid "extensions" to ESLint
    if (config.plugins.has('eslint')) {
      config.plugin('eslint').tap((args) => {
        if (args[0]) {
          delete args[0].extensions;
        }
        return args;
      });
    }
    
    // Configure TypeScript
    config.module
      .rule('ts')
      .test(/\.tsx?$/)
      .use('babel-loader')
      .loader('babel-loader')
      .options({
        presets: [
          '@babel/preset-typescript'
        ]
      })
      .end();
  },
});