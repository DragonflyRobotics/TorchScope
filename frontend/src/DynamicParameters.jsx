import SnappableResizable from "./SnappableResizable";
import Parameter from "./Parameter";




function DynamicParameters() {
    return (
        <SnappableResizable>
            <div className="bg-white h-full w-full flex flex-col items-center rounded-lg shadow-lg p-5">
                <h2 className="text-2xl font-bold mb-4">Dynamic Parameters</h2>
                <div className="flex flex-wrap justify-center overflow-y-auto h-full">
                    <Parameter />
                    <Parameter />
                    <Parameter />
                </div>
            </div>
        </SnappableResizable>
    );
}
export default DynamicParameters;
