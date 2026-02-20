import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, Input, Textarea, Button } from "@heroui/react";
import { Icon } from "@iconify/react";
import { personalInfoSchema, type PersonalInfoFormData } from "../types/personal-info";

export function PersonalInfoForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PersonalInfoFormData>({
    resolver: zodResolver(personalInfoSchema),
  });

  const onSubmit = (data: PersonalInfoFormData) => {
    console.log(data);
  };

  return (
    <Form 
      className="space-y-6 bg-content1 p-8 rounded-lg shadow-lg"
      onSubmit={handleSubmit(onSubmit)}
    >
      <h1 className="text-2xl font-bold text-foreground mb-6">
        Personal Information
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input
          label="First Name"
          placeholder="Enter first name"
          errorMessage={errors.firstName?.message}
          isInvalid={!!errors.firstName}
          {...register("firstName")}
          startContent={
            <Icon 
              icon="lucide:user" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          label="Last Name"
          placeholder="Enter last name"
          errorMessage={errors.lastName?.message}
          isInvalid={!!errors.lastName}
          {...register("lastName")}
          startContent={
            <Icon 
              icon="lucide:user" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          type="email"
          label="Email"
          placeholder="Enter email"
          errorMessage={errors.email?.message}
          isInvalid={!!errors.email}
          {...register("email")}
          startContent={
            <Icon 
              icon="lucide:mail" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          type="tel"
          label="Phone"
          placeholder="Enter phone number"
          errorMessage={errors.phone?.message}
          isInvalid={!!errors.phone}
          {...register("phone")}
          startContent={
            <Icon 
              icon="lucide:phone" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          type="date"
          label="Date of Birth"
          placeholder="Select date of birth"
          errorMessage={errors.dateOfBirth?.message}
          isInvalid={!!errors.dateOfBirth}
          {...register("dateOfBirth")}
        />

        <Input
          label="City"
          placeholder="Enter city"
          errorMessage={errors.city?.message}
          isInvalid={!!errors.city}
          {...register("city")}
          startContent={
            <Icon 
              icon="lucide:landmark" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          label="Country"
          placeholder="Enter country"
          errorMessage={errors.country?.message}
          isInvalid={!!errors.country}
          {...register("country")}
          startContent={
            <Icon 
              icon="lucide:globe" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />
      </div>

      <Textarea
        label="Address"
        placeholder="Enter your full address"
        errorMessage={errors.address?.message}
        isInvalid={!!errors.address}
        {...register("address")}
        minRows={2}
      />

      <Textarea
        label="Bio"
        placeholder="Tell us about yourself"
        errorMessage={errors.bio?.message}
        isInvalid={!!errors.bio}
        {...register("bio")}
        minRows={4}
      />

      <div className="flex justify-end gap-4">
        <Button
          type="button"
          variant="flat"
          color="default"
          startContent={<Icon icon="lucide:x" />}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          color="primary"
          startContent={<Icon icon="lucide:save" />}
        >
          Save Information
        </Button>
      </div>
    </Form>
  );
}