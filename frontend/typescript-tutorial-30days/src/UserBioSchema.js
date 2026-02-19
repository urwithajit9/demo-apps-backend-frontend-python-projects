"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var zod_1 = require("zod");
var UserBioSchema = zod_1.z.string().min(25).max(120);
var userBio = "I'm John Doe, a Web developer and a Tech writer.";
try {
    var parsedUserBio = UserBioSchema.parse(userBio);
    console.log("Validation passed: ", parsedUserBio);
}
catch (error) {
    if (error instanceof zod_1.z.ZodError) {
        console.error("Validation failed: ", error.issues[0]);
    }
    else {
        console.error("Unexpected error: ", error);
    }
}
