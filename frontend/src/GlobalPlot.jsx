// components/GlobalPlot.jsx or .tsx
import Plot from "react-plotly.js";
import { useResizeDetector } from "react-resize-detector";

const defaultLayout = {
  font: {
    family: "Inter, sans-serif",
    size: 12,
    color: "#333",
  },
  paper_bgcolor: "transparent",
  plot_bgcolor: "transparent",
  margin: { t: 30, l: 30, r: 30, b: 30 },
};

const defaultConfig = {
  displayModeBar: false,
  responsive: true,
};

export default function GlobalPlot({ data, layout = {}, config = {} }) {
  const { width, height, ref } = useResizeDetector();

  return (
    <div ref={ref} className="w-full h-full overflow-hidden">
      {width && height && (
        <Plot
          data={data}
          layout={{
            ...defaultLayout,
            ...layout,
            width,
            height,
            autosize: false,
          }}
          config={{ ...defaultConfig, ...config }}
        />
      )}
    </div>
  );
}

