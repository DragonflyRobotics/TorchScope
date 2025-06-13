import ResponsivePlot from "../ResponsivePlot";
import SnappableResizable from "../SnappableResizable";

function LinePlot({x, y, name}) {
    const plot_data = 
        {
            mode: 'lines+markers',
            marker: { color: "#ee6b3c" },
        };

    const plot_font = {
        font: {
            family: "Inter, sans-serif",
            size: 14,
            color: "#000",
        },
    };
    return (
        <SnappableResizable>
            <ResponsivePlot
                data={[{
                    x,
                    y,
                    type: 'scatter',
                    ...plot_data

                }]}
                layout={{
                    title: {
                        text: name,
                    },
                    ...plot_font,
                }}
            />
        </SnappableResizable>

    )
}

export default LinePlot;
