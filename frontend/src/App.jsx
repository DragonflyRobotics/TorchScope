// App.jsx or App.tsx
import Navbar from "./Navbar";
import GridBackground from "./GridBackground";
import LinePlot from "./plots/LinePlot";
import DynamicParameters from "./DynamicParameters";    


function App() {
    return (
        <div className="bg-base w-screen h-screen flex flex-col items-center pr-8 pl-8">
            <Navbar />
            <div className="w-full h-full relative">
                <GridBackground />
                    <LinePlot
                        x={[1, 2, 3, 4, 5]}
                        y={[10, 15, 13, 17, 22]}
                    />
                    <LinePlot
                        x={[1, 2, 3, 4, 5]}
                        y={[10, 15, 13, 17, 22]}
                    />
                    <DynamicParameters /> 
            </div>
        </div>
    );
}



export default App;

