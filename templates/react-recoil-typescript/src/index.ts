import React from "react";
import ReactDOM from "react-dom";
import { RecoilRoot } from "recoil";

import App from "./App";

ReactDOM.render(
    React.createElement(RecoilRoot, null, React.createElement(App)),
    document.querySelector("main#app-root")
);
