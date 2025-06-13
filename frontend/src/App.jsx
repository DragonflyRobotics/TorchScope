import Navbar from "./Navbar";

function App() {
    return (
        <div className="bg-base w-screen h-screen flex flex-col items-center pr-8 pl-8">
            <Navbar />
            <div className="w-full h-full">
                <GridBackground />
            </div>
        </div>
    );
}

function GridBackground() {
  return (
    <div
      className="w-full h-full"
      style={{
        backgroundColor: "rgba(255, 255, 255, 0.5)",
        backgroundImage: `
          linear-gradient(#d95d16 2px, transparent 2px),
          linear-gradient(90deg, #d95d16 2px, transparent 2px),
          linear-gradient(rgba(150, 150, 150, 0.3) 1px, transparent 1px),
          linear-gradient(90deg, rgba(150, 150, 150, 0.3) 1px, transparent 1px)
        `,
        backgroundSize: "100px 100px, 100px 100px, 20px 20px, 20px 20px",
        backgroundPosition: "-2px -2px, -2px -2px, -1px -1px, -1px -1px",
      }}
    />
  );
}


export default App;

