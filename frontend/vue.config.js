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
                    test: /\.vue$/, // Handle .vue files
                    loader: 'vue-loader',
                    options: {
                        compilerOptions: {
                          // Ensure the template compiler doesn’t generate TypeScript annotations
                          preserveWhitespace: false
                        }
                      }
                }
            ]
        }
    },
    chainWebpack: (config) => {
        // Modify the vue-loader rule to ensure <script lang="ts"> is processed by babel-loader
        config.module
            .rule('vue')
            .use('vue-loader')
            .tap((options) => {
                options.compilerOptions = options.compilerOptions || {};
                return options;
            });

        // Add a rule to process <script lang="ts"> in .vue files with babel-loader
        config.module
            .rule('ts-in-vue')
            .test(/\.vue$/)
            .include
            .add(/src/)
            .end()
            .use('babel-loader')
            .loader('babel-loader')
            .end();
    }
});
