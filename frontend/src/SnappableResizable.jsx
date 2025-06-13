import { Rnd } from "react-rnd";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUpDownLeftRight } from "@fortawesome/free-solid-svg-icons";

function snapToGrid(value, gridSize) {
    return Math.round(value / gridSize) * gridSize;
}

function SnappableResizable({ children }) {
    const gridSize = 100;
    const [size, setSize] = useState({ width: 400, height: 300 });
    //Not actual max width/height, just for random positioning
    const maxWidth = snapToGrid(window.innerWidth - 2 * gridSize, gridSize); // 50px padding
    const maxHeight = snapToGrid(window.innerHeight - 2 * gridSize, gridSize); // 50px padding
    const randomPositionX = Math.floor(Math.random() * (maxWidth / gridSize)) * gridSize;
    const randomPositionY = Math.floor(Math.random() * (maxHeight / gridSize)) * gridSize;
    const [position, setPosition] = useState({ 
        x: randomPositionX,
        y: randomPositionY,
    });

    return (
        <Rnd
            size={size}
            position={position}
            dragHandleClassName="custom-drag-handle"
            onDragStop={(e, d) => {
                setPosition({
                    x: Math.round(d.x / gridSize) * gridSize,
                    y: Math.round(d.y / gridSize) * gridSize,
                });
            }}
            onResizeStop={(e, direction, ref, delta, pos) => {
                setSize({
                    width: Math.round(ref.offsetWidth / gridSize) * gridSize,
                    height: Math.round(ref.offsetHeight / gridSize) * gridSize,
                });
                setPosition({
                    x: Math.round(pos.x / gridSize) * gridSize,
                    y: Math.round(pos.y / gridSize) * gridSize,
                });
            }}
            bounds="parent"
            className="z-10"
        >
            <div className="w-full h-full relative shadow-lg rounded-lg border border-primary-translucent">
                <div className="custom-drag-handle absolute top-0 left-0 p-2 cursor-move z-20">
                    <div className="w-5 h-5 bg-primary-translucent rounded-full flex items-center justify-center">
                        <FontAwesomeIcon className="w-3 h-3" icon={faUpDownLeftRight} />
                    </div>
                </div>
                <div className="w-full h-full overflow-hidden">{children}</div>
            </div>
        </Rnd>
    );
}

export default SnappableResizable;
