"use client";
import { useState } from "react";
import { motion } from "framer-motion";

interface AgeData {
  [key: string]: { percentage: number; male: number; female: number };
}

interface AgeStructureProps {
  data: AgeData;
}

const AgeStructure = ({ data }: AgeStructureProps) => {
  const [openGroup, setOpenGroup] = useState<string | null>(null);

  const toggleGroup = (group: string) => {
    setOpenGroup(openGroup === group ? null : group);
  };

  return (
    <div className="max-w-lg mx-auto bg-white shadow-lg rounded-xl p-6">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">
        Age Structure
      </h2>
      <div className="space-y-3">
        {Object.entries(data).map(([group, { percentage, male, female }]) => (
          <div key={group} className="border rounded-lg p-4 bg-gray-100">
            <button
              onClick={() => toggleGroup(group)}
              className="w-full text-left flex justify-between items-center text-lg font-medium"
            >
              <span>
                {group} ({percentage}%)
              </span>
              <span className="text-gray-600">
                {openGroup === group ? "▼" : "▶"}
              </span>
            </button>

            {openGroup === group && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-3 text-gray-700"
              >
                <p>👨 Male: {male.toLocaleString()}</p>
                <p>👩 Female: {female.toLocaleString()}</p>
              </motion.div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgeStructure;
