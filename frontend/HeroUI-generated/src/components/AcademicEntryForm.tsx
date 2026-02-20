import React from "react";
import { useFieldArray, useFormContext } from "react-hook-form";
import { Input, Switch, Button, Card } from "@heroui/react";
import { Icon } from "@iconify/react";
import type { AcademicInfoFormData } from "../types/academic-info";

interface AcademicEntryFormProps {
  index: number;
  onRemove: () => void;
}

export function AcademicEntryForm({ index, onRemove }: AcademicEntryFormProps) {
  const {
    register,
    control,
    watch,
    formState: { errors },
  } = useFormContext<AcademicInfoFormData>();

  const { fields, append, remove } = useFieldArray({
    control,
    name: `academics.${index}.publications`,
  });

  const currentlyStudying = watch(`academics.${index}.currentlyStudying`);
  const academicErrors = errors.academics?.[index];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input
          label="Degree"
          placeholder="Enter degree name"
          errorMessage={academicErrors?.degree?.message}
          isInvalid={!!academicErrors?.degree}
          {...register(`academics.${index}.degree`)}
          startContent={
            <Icon 
              icon="lucide:graduation-cap" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          label="Field of Study"
          placeholder="Enter field of study"
          errorMessage={academicErrors?.fieldOfStudy?.message}
          isInvalid={!!academicErrors?.fieldOfStudy}
          {...register(`academics.${index}.fieldOfStudy`)}
          startContent={
            <Icon 
              icon="lucide:book-open" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          label="Institution"
          placeholder="Enter institution name"
          errorMessage={academicErrors?.institution?.message}
          isInvalid={!!academicErrors?.institution}
          {...register(`academics.${index}.institution`)}
          startContent={
            <Icon 
              icon="lucide:building-2" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          type="date"
          label="Start Date"
          placeholder="Select start date"
          errorMessage={academicErrors?.startDate?.message}
          isInvalid={!!academicErrors?.startDate}
          {...register(`academics.${index}.startDate`)}
        />

        <div className="flex items-center gap-4">
          <Switch
            {...register(`academics.${index}.currentlyStudying`)}
          >
            I am currently studying
          </Switch>
        </div>

        {!currentlyStudying && (
          <Input
            type="date"
            label="End Date"
            placeholder="Select end date"
            errorMessage={academicErrors?.endDate?.message}
            isInvalid={!!academicErrors?.endDate}
            {...register(`academics.${index}.endDate`)}
          />
        )}

        <Input
          label="GPA"
          placeholder="Enter GPA (optional)"
          {...register(`academics.${index}.gpa`)}
          startContent={
            <Icon 
              icon="lucide:award" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Publications</h2>
          <Button
            type="button"
            color="primary"
            variant="flat"
            size="sm"
            startContent={<Icon icon="lucide:plus" />}
            onPress={() => append({ title: "", journal: "", year: "", url: "" })}
          >
            Add Publication
          </Button>
        </div>

        {fields.map((field, pubIndex) => (
          <Card key={field.id} className="p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                label="Title"
                placeholder="Enter publication title"
                errorMessage={errors.academics?.[index]?.publications?.[pubIndex]?.title?.message}
                isInvalid={!!errors.academics?.[index]?.publications?.[pubIndex]?.title}
                {...register(`academics.${index}.publications.${pubIndex}.title`)}
              />

              <Input
                label="Journal"
                placeholder="Enter journal name"
                errorMessage={errors.academics?.[index]?.publications?.[pubIndex]?.journal?.message}
                isInvalid={!!errors.academics?.[index]?.publications?.[pubIndex]?.journal}
                {...register(`academics.${index}.publications.${pubIndex}.journal`)}
              />

              <Input
                label="Year"
                placeholder="Enter publication year"
                errorMessage={errors.academics?.[index]?.publications?.[pubIndex]?.year?.message}
                isInvalid={!!errors.academics?.[index]?.publications?.[pubIndex]?.year}
                {...register(`academics.${index}.publications.${pubIndex}.year`)}
              />

              <Input
                label="URL (optional)"
                placeholder="Enter publication URL"
                errorMessage={errors.academics?.[index]?.publications?.[pubIndex]?.url?.message}
                isInvalid={!!errors.academics?.[index]?.publications?.[pubIndex]?.url}
                {...register(`academics.${index}.publications.${pubIndex}.url`)}
              />

              <Button
                type="button"
                color="danger"
                variant="flat"
                size="sm"
                className="mt-2"
                startContent={<Icon icon="lucide:trash-2" />}
                onPress={() => remove(pubIndex)}
              >
                Remove
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <Button
        type="button"
        color="danger"
        variant="flat"
        startContent={<Icon icon="lucide:trash-2" />}
        onPress={onRemove}
      >
        Remove Academic Entry
      </Button>
    </div>
  );
}