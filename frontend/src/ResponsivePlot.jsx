import Plot from "react-plotly.js";
import { useResizeDetector } from "react-resize-detector";
import { useRef, useEffect, useState } from "react";

function ResponsivePlot({ data, layout, config }) {
    const { width, height, ref } = useResizeDetector();
    const plotRef = useRef(null);
    const [userLayout, setUserLayout] = useState({});

    // Handle user zoom/pan
    const handleRelayout = (newLayout) => {
        // Only store keys that affect view like axis ranges
        const { 'xaxis.range[0]': x0, 'xaxis.range[1]': x1, 'yaxis.range[0]': y0, 'yaxis.range[1]': y1 } = newLayout;
        if (x0 !== undefined && x1 !== undefined && y0 !== undefined && y1 !== undefined) {
            setUserLayout({
                xaxis: { range: [x0, x1] },
                yaxis: { range: [y0, y1] },
            });
        }
    };

    return (
        <div ref={ref} className="w-full h-full overflow-hidden rounded-lg shadow-lg">
            {width && height ? (
                <Plot
                    ref={plotRef}
                    data={data}
                    layout={{
                        ...layout,
                        ...userLayout,
                        width,
                        height,
                        autosize: false,
                        margin: { t: 60, l: 30, r: 30, b: 30 },
                    }}
                    config={{ responsive: true, ...config }}
                    onRelayout={handleRelayout}
                />
            ) : null}
        </div>
    );
}
export default ResponsivePlot;
