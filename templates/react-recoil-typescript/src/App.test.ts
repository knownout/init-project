import React from "react";
import { cleanup, fireEvent, render } from "@testing-library/react";
import { RecoilRoot } from "recoil";
import App from "./App";

afterEach(cleanup);
it("Application span text changes after click on h1 element", () => {
    const { queryByText, getByText } = render(
        React.createElement(RecoilRoot, null, React.createElement(App))
    );

    expect(queryByText(/is clicked: false/i))
        .toBeTruthy();

    fireEvent.click(getByText("Hello world"));
    expect(queryByText(/is clicked: true/i))
        .toBeTruthy();

    fireEvent.click(getByText("Hello world"));
    expect(queryByText(/is clicked: true/i))
        .toBeTruthy();
});
