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
      title: 'Rivue.ai | Learn anything'
    }
  },
  configureWebpack: {
    resolve: {
      extensions: ['.ts', '.js', '.vue', '.json']
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          loader: 'babel-loader',
          exclude: /node_modules/
        },
        {
          test: /\.vue$/,
          loader: 'vue-loader'
        }
      ]
    }
  },
  chainWebpack: (config) => {
    // Ensure vue-loader processes .vue files correctly
    config.module
      .rule('vue')
      .use('vue-loader')
      .tap((options) => {
        options.compilerOptions = options.compilerOptions || {};
        options.compilerOptions.preserveWhitespace = false;
        return options;
      });

    // Add a custom rule to process <script lang="ts"> in .vue files with babel-loader
    config.module
      .rule('ts-in-vue')
      .test(/\.vue$/)
      .use('babel-loader')
      .loader('babel-loader')
      .end();
  }
});