import React, { Suspense } from "react";
import { RecoilRoot, atom, useRecoilState } from "recoil";

const Helmet = React.lazy(() => import("react-helmet"));

import "./App.scss";

const titleClickedState = atom<boolean>({
    key: "titleClickedState",
    default: false
});

export default function App () {
    const [ clicked, setClicked ] = useRecoilState(titleClickedState);

    return <Suspense fallback={ <div>Loading...</div> }>
        <Helmet>
            <title>Website loaded</title>
        </Helmet>

        <h1 onClick={ () => setClicked(true) }>Hello world</h1>
        <span>Is clicked: { String(clicked) }</span>
    </Suspense>;
}
