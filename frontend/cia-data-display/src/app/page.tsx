import AgeStructure from "./components/AgeStructure";
import Argiproduct from "./components/Argiproduct";

const ageData = {
  "0-14 years:": { percentage: 24.5, male: 1018005046, female: 958406907 },
  "15-64 years:": { percentage: 68.7, male: 2658595672, female: 2592930538 },
  "65 years and over": { percentage: 6.8, male: 44101180, female: 52102662 },
};

const productsList = [
  [
    "Sugarcane",
    "Beef",
    "Maize",
    "Cabbages",
    "Potatoes",
    "Tomatoes",
    "Milk",
    "Onions",
    "Bananas",
    "Wheat",
  ],
  [
    "Milk",
    "Sugarcane",
    "Maize",
    "Rice",
    "Plantains",
    "Oil palm fruit",
    "Bananas",
    "Chicken",
    "Pineapples",
    "Potatoes",
  ],
];

export default function Home() {
  return (
    <div>
      <main className="flex min-h-screen items-center justify-center bg-gray-50">
        {/* <h2>Country: India</h2> */}
        <AgeStructure data={ageData} />
        {productsList.map((products, index) => (
          <Argiproduct products={products} />
        ))}
      </main>
    </div>
  );
}
