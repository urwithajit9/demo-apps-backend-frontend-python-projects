import { z } from "zod";

// const UserBioSchema = z.string().min(25).max(120);
//let userBio = "I'm John Doe, a Web developer and a Tech writer.";

const UserBioSchema = z
  .string()
  .min(25, "Bio must be at least 25 characters long")
  .max(120, "Bio must not exceet 120 characters");

// Simple email validation
const UserEmailSchema = z.string().email().trim();

// A Terms & Conditions check at runtime
const TacSchema = z.boolean();

// Large high-precision values if they are being calculated at runtime
const FactorialSchema = z.bigint();

let userBio = "I'm John.";
let userEmail = "ajitkumar.pu@example";

try {
  //const parsedUserBio = UserBioSchema.parse(userBio);
  //console.log("Validation passed: ", parsedUserBio);
  const parsedUserEmail = UserEmailSchema.parse(userEmail);
  console.log("Validation passed: ", parsedUserEmail);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error("Validation failed: ", error.issues[0]);
  } else {
    console.error("Unexpected error: ", error);
  }
}
