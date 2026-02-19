import React, { useState } from "react";
function getRandomNumber(): number {
  return Math.floor(Math.random() * 6) + 1;
}

export default function GuessTheNumber() {
  const [inputNumber, setInputnumber] = useState<number>(0);
  const [randomNumber, setRandomNumber] = useState<number>(0);
  const [isSuccess, setIsSuccess] = useState(false);
  const [isCheck, setIsCheck] = useState(false);

  // Handle input change
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputnumber(Number(event.target.value)); // Update the state with the new input value
  };

  const handleClick = (event: React.MouseEvent) => {
    event.preventDefault();
    const random_number = getRandomNumber();
    setRandomNumber(random_number);
    setInputnumber(0);
    setIsSuccess((inputNumber as unknown as number) == randomNumber);
    setIsCheck(true);
  };

  const response = isSuccess
    ? "Contratualtions !You guessed correctly.!"
    : `Sorry ! Wrong Guess. Number was: ${randomNumber}`;

  return (
    <div>
      <div className="container">
        <h1>Guess The Number</h1>
        <p>Enter Your Number (1-6)</p>
        <form>
          <input
            type="text"
            value={inputNumber} // Bind the state to the input field
            onChange={handleInputChange} // Handle the change event
          />
          <button onClick={handleClick}>Check Your Guess!</button>
        </form>
        <p>{isCheck && response}</p>
      </div>
    </div>
  );
}
