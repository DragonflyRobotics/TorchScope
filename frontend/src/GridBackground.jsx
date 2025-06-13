function GridBackground() {
  return (
    <div
      className="absolute inset-0 z-0"
      style={{
        backgroundColor: "base",
        backgroundImage: `
          linear-gradient(#d95d16 1px, transparent 1px),
          linear-gradient(90deg, #d95d16 1px, transparent 1px),
          linear-gradient(rgba(150, 150, 150, 0.2) 1px, transparent 1px),
          linear-gradient(90deg, rgba(150, 150, 150, 0.2) 1px, transparent 1px)
        `,
        backgroundSize: "100px 100px, 100px 100px, 20px 20px, 20px 20px",
        backgroundPosition: "-2px -2px, -2px -2px, -1px -1px, -1px -1px",
      }}
    />
  );
}
export default GridBackground;
