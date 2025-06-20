import SnappableResizable from "./SnappableResizable";
import { useAppData } from "./AppDataContext";

function ModelSVG() {
    const { modelSVG } = useAppData();
    if (!modelSVG) {
        return (
        <SnappableResizable>
            <div className="bg-white h-full w-full flex flex-col items-center rounded-lg shadow-lg p-5">
                <h2 className="text-2xl font-bold mb-4">Model SVG</h2>
                <p className="text-gray-500">No model SVG available</p>
            </div>
        </SnappableResizable>
        );
    }
    return (
        <SnappableResizable>
            <div className="bg-white h-full w-full flex flex-col items-center rounded-lg shadow-lg p-5" dangerouslySetInnerHTML={{ __html: modelSVG}} />
        </SnappableResizable>
    );
}

export default ModelSVG;
