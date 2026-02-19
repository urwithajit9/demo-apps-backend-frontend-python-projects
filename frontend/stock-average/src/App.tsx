import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function App() {
  const [currentShares, setCurrentShares] = useState("");
  const [currentPrice, setCurrentPrice] = useState("");
  const [newPrice, setNewPrice] = useState("");
  const [targetPrice, setTargetPrice] = useState("");
  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState("");

  const handleCalculate = () => {
    const cs = parseFloat(currentShares);
    const cp = parseFloat(currentPrice);
    const np = parseFloat(newPrice);
    const tp = parseFloat(targetPrice);

    if (!cs || !cp || !np || !tp) {
      setError("Please fill in all fields with valid numbers.");
      setResult(null);
      return;
    }

    if (tp <= np) {
      setError("Target price must be higher than new price to average down.");
      setResult(null);
      return;
    }

    const x = (cs * (cp - tp)) / (tp - np);

    setError("");
    setResult(x > 0 ? Math.ceil(x) : 0);
  };

  return (
    <main className="min-h-screen flex items-center justify-center px-4 bg-gray-100 py-10">
      <Card className="w-full max-w-md mx-auto shadow-lg rounded-2xl p-6 bg-white">
        <h1 className="text-2xl font-semibold text-center mb-6">
          📉 Stock Average Calculator
        </h1>
        <CardContent className="flex flex-col space-y-4">
          <Input
            type="number"
            placeholder="Current Shares (e.g. 5855)"
            value={currentShares}
            onChange={(e) => setCurrentShares(e.target.value)}
          />
          <Input
            type="number"
            placeholder="Current Price (e.g. 10.87)"
            value={currentPrice}
            onChange={(e) => setCurrentPrice(e.target.value)}
          />
          <Input
            type="number"
            placeholder="New Stock Price (e.g. 6.63)"
            value={newPrice}
            onChange={(e) => setNewPrice(e.target.value)}
          />
          <Input
            type="number"
            placeholder="Target Average Price (e.g. 6.63)"
            value={targetPrice}
            onChange={(e) => setTargetPrice(e.target.value)}
          />
          <Button onClick={handleCalculate} className="w-full text-lg">
            Calculate
          </Button>

          {error && <p className="text-sm text-red-500 text-center">{error}</p>}

          {result !== null && !error && (
            <div className="text-center text-green-600 font-semibold text-lg">
              📊 You need to buy <span className="font-bold">{result}</span>{" "}
              shares
            </div>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
