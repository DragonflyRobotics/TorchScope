import { Slider } from "@/components/ui/slider";
import React from 'react';
import { useState } from 'react';

export function ColorSlider({ value, setCurrentValue, min = 0, max = 100, step = 1 }) {
    return (
        <Slider
            value={[value]}
            onValueChange={(val) => setCurrentValue(val[0])}
            min={min} 
            max={max}
            step={step}
        />
    )
}

function Parameter({name = "Parameter 1", min = 0, max = 100, step = 1, startValue = 50}) {
    // This component represents a single parameter with a slider.
    const [currentValue, setCurrentValue] = useState(startValue);
    return (
        <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
                <label className="block mb-2 text-sm font-medium text-gray-700">{name}</label>
                <span className="text-sm text-gray-500">Value: {currentValue}</span>
            </div>
            <ColorSlider value={currentValue} setCurrentValue={setCurrentValue} min={min} max={max} step={step} />
        </div>
    )
}
export default Parameter;
