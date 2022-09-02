import jwt_decode from "jwt-decode";
import dayjs from "dayjs";

export default function useComp1(initialParam = "Composable data") {
  const err = {
    msg: "Hmm... Something went wrong, please check your network connection and try again!",
    val: false,
    msg1: "You are already logged in!",
    val1: true,
    msg2: "You are not logged in!",
  };

  const Url = "unknown";

  async function unSecFetcher(speUrl, config = {}) {
    config["headers"] = {
      "Content-Type": "application/json",
    };
    const res = await fetch(`${Url}${speUrl}`, config);
    const data = await res.json();

    return { res, data };
  }

  async function secFetcher(speUrl, config) {
    const res = await fetch(`${Url}${speUrl}`, config);
    const data = await res.json();

    return { res, data };
  }

  const refFunc = async (ref) => {
    let response = await fetch(`${Url}user/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${ref}`,
      },
    });
    let data = await response.json();
    localStorage.setItem("acc", data.access_token);
    return data.access_token;
  };

  const customFetcher = async (speUrl, config = {}) => {
    let acc = localStorage.getItem("acc") ? localStorage.getItem("acc") : null;

    const user = jwt_decode(acc);
    const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

    if (isExpired) {
      acc = await refFunc(localStorage.getItem("ref"));
    }

    config["headers"] = {
      Authorization: `Bearer ${localStorage.getItem("acc")}`,
      "Content-Type": "application/json",
    };

    let { res, data } = await secFetcher(speUrl, config);
    return { res, data };
  };

  return { unSecFetcher, customFetcher, err };
}
