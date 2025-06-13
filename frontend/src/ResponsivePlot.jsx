import Plot from "react-plotly.js";
import { useResizeDetector } from "react-resize-detector";

function ResponsivePlot({ data, layout, config }) {
    const { width, height, ref } = useResizeDetector();

    return (
        <div ref={ref} className="w-full h-full overflow-hidden rounded-lg shadow-lg">
            {width && height ? (
                <Plot
                    data={data}
                    layout={{
                        ...layout,
                        width,
                        height,
                        autosize: false,
                        margin: { t: 60, l: 30, r: 30, b: 30 },
                    }}
                    config={{ responsive: true, ...config }}
                />
            ) : null}
        </div>
    );
}
export default ResponsivePlot;
