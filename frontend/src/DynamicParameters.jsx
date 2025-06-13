import SnappableResizable from "./SnappableResizable";
import { Slider } from "@/components/ui/slider";

export function ColorSlider() {
  return (
    <Slider
      defaultValue={[50]}
      max={100}
      step={1}
      className="bg-red-500"
      thumbClassName="bg-red-500 hover:bg-red-600"
      trackClassName="bg-red-200"
      rangeClassName="bg-red-500"
    />
  )
}


function DynamicParameters() {
    return (
        <SnappableResizable>
            <div className="bg-white h-full w-full flex flex-col items-center rounded-lg shadow-lg p-5">
                <h2 className="text-2xl font-bold mb-4">Dynamic Parameters</h2>
                <div className="flex flex-wrap justify-center overflow-y-auto h-full">
                    <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
                        <div className="flex items-center justify-between mb-4">
                            <label className="block mb-2 text-sm font-medium text-gray-700">Parameter 1</label>
                            <span className="text-sm text-gray-500">Value: 50</span>
                        </div>
                        <ColorSlider defaultValue={[50]} />
                    </div>
                    <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
                        <div className="flex items-center justify-between mb-4">
                            <label className="block mb-2 text-sm font-medium text-gray-700">Parameter 1</label>
                            <span className="text-sm text-gray-500">Value: 50</span>
                        </div>
                        <ColorSlider defaultValue={[50]} />
                    </div>
                    <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
                        <div className="flex items-center justify-between mb-4">
                            <label className="block mb-2 text-sm font-medium text-gray-700">Parameter 1</label>
                            <span className="text-sm text-gray-500">Value: 50</span>
                        </div>
                        <ColorSlider defaultValue={[50]} />
                    </div>
                    <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
                        <div className="flex items-center justify-between mb-4">
                            <label className="block mb-2 text-sm font-medium text-gray-700">Parameter 1</label>
                            <span className="text-sm text-gray-500">Value: 50</span>
                        </div>
                        <ColorSlider defaultValue={[50]} />
                    </div>
                    <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
                        <div className="flex items-center justify-between mb-4">
                            <label className="block mb-2 text-sm font-medium text-gray-700">Parameter 1</label>
                            <span className="text-sm text-gray-500">Value: 50</span>
                        </div>
                        <ColorSlider defaultValue={[50]} />
                    </div>
                </div>
            </div>
        </SnappableResizable>
    );
}
export default DynamicParameters;
