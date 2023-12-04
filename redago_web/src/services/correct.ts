import axios from "axios";

const correct = (text: string) => {
  return axios.post("http://127.0.0.1:31416/correct-with-reason", { text });
};

export default correct;
