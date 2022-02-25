import { Configuration as WebpackConfiguration } from "webpack";
import * as path from "path";

import HtmlWebpackPlugin = require("html-webpack-plugin");
import MiniCssExtractPlugin = require("mini-css-extract-plugin");
import CopyWebpackPlugin = require("copy-webpack-plugin");
import TerserWebpackPlugin = require("terser-webpack-plugin");

const isProduction = process.env.NODE_ENV === "production";

const stylesHandler = isProduction ? MiniCssExtractPlugin.loader : "style-loader";


const config = {
    entry: "./src/index.ts",
    output: {
        path: path.resolve(__dirname, "dist")
    },
    devServer: {
        host: "0.0.0.0",
        port: 8080,

        hot: true,
        static: "/public/",

        historyApiFallback: true,
        open: false
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: "./src/index.html",
            filename: "index.html",
            inject: true
        }),
        new CopyWebpackPlugin({
            patterns: [
                { from: "public", to: "public", filter: (path: string) => !path.includes("sw.js") }
                // { from: "public/sw.js", to: "" }
            ]
        }),
        new TerserWebpackPlugin({
            terserOptions: {
                output: {
                    comments: false
                }
            },

            extractComments: false
        })
    ],
    module: {
        rules: [
            {
                test: /\.(ts|tsx)$/i,
                loader: "ts-loader",
                exclude: [ "/node_modules/" ]
            },
            {
                test: /\.s[ac]ss$/i,
                use: [ stylesHandler, "css-loader", "postcss-loader", "sass-loader" ]
            },
            {
                test: /\.css$/i,
                use: [ stylesHandler, "css-loader", "postcss-loader" ]
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2|png|jpg|gif)$/i,
                type: "asset"
            },
            {
                test: /\.(js|jsx)$/i,
                loader: "babel-loader",
                exclude: [ "/node_modules/" ]
            }
        ]
    },
    resolve: {
        extensions: [ ".tsx", ".ts", ".js" ]
    }
} as WebpackConfiguration;

module.exports = () => {
    if (isProduction) {
        config.mode = "production";

        if (!config.plugins) config.plugins = [];

        config.plugins.push(new MiniCssExtractPlugin());

    } else {
        config.mode = "development";
    }
    return config;
};
