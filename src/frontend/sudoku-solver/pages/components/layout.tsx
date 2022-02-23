import { FC } from "react";
import styled from "styled-components";

const Children = styled.div`
    background-image: linear-gradient(to right, rgb(127, 127, 213), rgb(134, 168, 231), rgb(145, 234, 228));
`;

const Layout: FC = ({ children }) => {
    return <div id="root">
        <Children>
            {children}
        </Children>
    </div>
}

export default Layout;