import { z } from "zod";

const publicationSchema = z.object({
  title: z.string().min(2, "Publication title must be at least 2 characters"),
  journal: z.string().min(2, "Journal name must be at least 2 characters"),
  year: z.string().min(4, "Year must be valid"),
  url: z.string().url("Must be a valid URL").optional(),
});

const academicEntrySchema = z.object({
  id: z.string(),
  degree: z.string().min(2, "Degree must be at least 2 characters"),
  fieldOfStudy: z.string().min(2, "Field of study must be at least 2 characters"),
  institution: z.string().min(2, "Institution must be at least 2 characters"),
  startDate: z.string().min(1, "Start date is required"),
  endDate: z.string().min(1, "End date is required").optional(),
  currentlyStudying: z.boolean(),
  gpa: z.string().optional(),
  publications: z.array(publicationSchema).optional(),
});

export const academicInfoSchema = z.object({
  academics: z.array(academicEntrySchema),
});

export type PublicationData = z.infer<typeof publicationSchema>;
export type AcademicEntryData = z.infer<typeof academicEntrySchema>;
export type AcademicInfoFormData = z.infer<typeof academicInfoSchema>;
