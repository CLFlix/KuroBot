export type Command = {
  name: string;
  description: string;
  category: string;
};

export type StatusMessage = {
  message: string;
  type: "error" | "success";
};
