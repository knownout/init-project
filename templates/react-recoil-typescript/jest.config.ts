import type { Config } from "@jest/types";

module.exports = {
    verbose: true,

    preset: "ts-jest",
    testEnvironment: "jsdom",

    testMatch: [
        "**/?(*.)(spec|test).ts?(x)"
    ],

    globals: {
        "ts-jest": {
            tsconfig: "tsconfig.json",
            diagnostics: false
        }
    }
} as Config.InitialOptions;
