import { useState } from "react";
function addMinutes(date: Date, minutes: number): Date {
  // Multiply minutes by 60000 to convert minutes to milliseconds
  return new Date(date.getTime() + minutes * 60000);
}

function Clock() {
  const [time, setTime] = useState(new Date());

  const handleClick = () => {
    setTime(addMinutes(time, 10));
  };

  return (
    <div>
      <p>{time.toLocaleTimeString()}</p>
      <button onClick={handleClick}>+ 10 Minutes</button>
    </div>
  );
}

export default Clock;
