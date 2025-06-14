import { Slider } from "@/components/ui/slider";
import React from 'react';
import { useState } from 'react';

export function ColorSlider({ value, setCurrentValue, min, max, step}) {
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

function onChangeHandler(name, setCurrentValue) {
    return (value) => {
        //send post request to the server with the new value 
        fetch('http://localhost:8000/api/update-parameter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name, value: value }),
        })
        setCurrentValue(value);
    }
}

function Parameter({name, min, max, step, startValue}) {
    // This component represents a single parameter with a slider.
    const [currentValue, setCurrentValue] = useState(startValue);
    if (currentValue !== startValue) {
        setCurrentValue(startValue);
    }
    return (
        <div className="w-full m-1 border border-gray-200 rounded-lg p-6">
            <div className="flex items-center justify-between mb-4">
                <label className="block mb-2 text-sm font-medium text-gray-700">{name}</label>
                <span className="text-sm text-gray-500">Value: {currentValue}</span>
            </div>
            <ColorSlider value={currentValue} setCurrentValue={onChangeHandler(name, setCurrentValue)} min={min} max={max} step={step} />
        </div>
    )
}
export default Parameter;
