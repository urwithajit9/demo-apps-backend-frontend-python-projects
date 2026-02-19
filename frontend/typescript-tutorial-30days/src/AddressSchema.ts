import { z } from "zod";

const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  zipCode: z.string().length(5),
});

// const validateAddress = (address: unknown) => {
//   try {
//     const parsedAddress = AddressSchema.parse(address);
//     console.log("Validation passed: ", parsedAddress);
//   } catch (error) {
//     if (error instanceof z.ZodError) {
//       for (const issue of error.issues) {
//         console.error("Validation failed: ", issue.message);
//       }
//     } else {
//       console.error("Unexpected error: ", error);
//     }
//   }
// };

type Address = z.infer<typeof AddressSchema>;

const validateAddress = (address: Address) => {
  const isValidAddress = AddressSchema.parse(address);
  console.log("Validation passed: ", isValidAddress);
  return isValidAddress;
};

let myaddress: Address = {
  street: "123 Main St",
  city: "Anytown",
  zipCode: "12345",
};
validateAddress(myaddress);

// Simple email validation
const UserEmailSchema = z.string().email().trim();

// A Terms & Conditions check at runtime
const TacSchema = z.boolean();

// Large high-precision values if they are being calculated at runtime
const FactorialSchema = z.bigint();

const PositiveNumberSchema = z.number().positive();

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: UserEmailSchema,
  address: AddressSchema,
  age: PositiveNumberSchema,
});

const CustomerSchema = UserSchema.extend({
  loyaltyPoints: z.number().int().nonnegative(),
});

const ProductSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  price: PositiveNumberSchema,
});

const InventoryItemSchema = z.object({
  quantity: z.number().int().nonnegative(),
  location: z.string(),
});

const StockItemSchema = ProductSchema.merge(InventoryItemSchema);

// Zod records are useful for representing a collection of items where the key is a unique identifier
// and the value is the item itself.
// For example, a cart of products where the key is the product ID and the value is the quantity of that product in the cart.
const CartSchema = z.record(z.string().uuid(), z.number().int().positive());

const PhoneNumberSchema = z.preprocess(
  (val) => (typeof val === "string" ? val.replace(/\D/g, "") : val),
  z.string().length(10)
);

const UserSchema2 = z.object({
  username: z.string().min(5, "Username must be at least 5 characters"),
  email: z.string().email("Invalid email format"),
  password: z.string().min(8, "Password must contain at least 8 characters"),
  age: z.number().optional(),
});

// Type inference in action
const validUserData = {
  username: "johnsmith",
  email: "john@example.com",
  password: "strongpassword123",
};

const myUser = UserSchema2.parse(validUserData);

// TypeScript infers the type of 'myUser' as:
// { username: string; email: string; password: string; age?: number }

const userInput = { username: "jane", email: "not-an-email" };

// parse will throw an error
try {
  UserSchema.parse(userInput);
} catch (error) {
  console.error("Validation failed:", error);
}
// safeParse returns a result
const result = UserSchema.safeParse(userInput);
if (!result.success) {
  console.error("Validation failed:", result.error);
}
