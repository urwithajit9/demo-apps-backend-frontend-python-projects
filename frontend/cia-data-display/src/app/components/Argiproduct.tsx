"use client";
import { motion } from "framer-motion";

interface ArgiproductProps {
  products: string[];
}

const Argiproduct = ({ products }: ArgiproductProps) => {
  return (
    <div className="max-w-xl mx-auto bg-white shadow-lg rounded-xl p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4 text-center">
        Agricultural Products
      </h2>
      <div className="grid grid-cols-2 gap-4">
        {products.map((item, index) => (
          <motion.div
            key={index}
            whileHover={{ scale: 1.05 }}
            className="p-4 bg-green-100 text-gray-700 text-center rounded-lg shadow-md"
          >
            {item}
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Argiproduct;
