import { Slider } from "@/components/ui/slider";
import React from 'react';
import { useState, useRef } from 'react';
import { useAppData } from "./AppDataContext";
import Loading from "./Loading";

export function ColorSlider({ value, onCommit, onChange, min, max, step}) {
    const isDragging = useRef(false);
    const [ undecidedValue, setUndecidedValue ] = useState(value);

    function handlePointerDown() {
        isDragging.current = true;
    }

    function handlePointerUp() {
        if (isDragging.current) {
            isDragging.current = false;
            onCommit(undecidedValue);
        }
    }
    return (
        <Slider
            value={[value]}
            onValueChange={(newValue) => {onChange(newValue[0]); setUndecidedValue(newValue[0]);}}
            onPointerDown={handlePointerDown}
            onPointerUp={handlePointerUp}
            onBlur={() => {
                // Handle keyboard interactions finishing
                if (isDragging.current) {
                    isDragging.current = false;
                    onCommit(undecidedValue);
                }
            }}
            min={min} 
            max={max}
            step={step}
        />
    )
}

function commitValue(name, setBarPos, updateParameter) {
    // Send the updated value to the backend
    return (value) => {
        updateParameter(name, value);
        setBarPos(value);
    }
}

function Parameter({name, min, max, step, startValue}) {
    // This component represents a single parameter with a slider.
    const [barPos, setBarPos] = useState(startValue);
    const { data, updateParameter } = useAppData();
    return (
        <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
                <label className="block mb-2 text-sm font-medium text-gray-700">{name}</label>
                <span className="text-sm text-gray-500">Value: {barPos}</span>
            </div>
            <ColorSlider value={barPos} onCommit={commitValue(name, setBarPos, updateParameter)} onChange={setBarPos} min={min} max={max} step={step} />
        </div>
    )
}
export default Parameter;
