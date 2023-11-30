import { cn } from "@/lib/utils"
import { useEffect, useState } from "react"

import type { ChatMessageSchema } from "~api/openapi/schemas"

import ChatMessage from "./chat-message"
import PromptForm from "./prompt-form"
import { Separator } from "./ui/separator"
import fetchEventSource from '@microsoft/fetch-event-source';

const Chat = () => {
  const [messages, setMessages] = useState<any[]>([
    {
      message:
        "Hi!\n\n I'm an assistant trained on this documentation!\n\n Ask me anything about `Airbyte`.",
      sender: "bot"
    }
  ])
  const showPopularQuestions = messages.length === 1


  useEffect(() => {
    const fetchData = async () => {
      await fetchEventSource(`http://127.0.0.1:8000/chat-stream/`, {
        method: "POST",
        headers: { Accept: "text/event-stream" },
        onopen(res) {
          if (res.ok && res.status === 200) {
            console.log("Connection made ", res);
          } else if (res.status >= 400 && res.status < 500 && res.status !== 429) {
            console.log("Client-side error ", res);
          }
        },
        onmessage(event) {
          console.log(event.data);
          const parsedData = JSON.parse(event.data);
          setMessages((messages) => [...messages, { message: parsedData, sender: "bot" }]); // Important to set the data this way, otherwise old data may be overwritten if the stream is too fast
        },
        onclose() {
          console.log("Connection closed by the server");
        },
        onerror(err) {
          console.log("There was an error from server", err);
        },
      });
    };
    fetchData();
  }, []);

  const sendMessage = async (message: string) => {
    setMessages((messages) => [...messages, { message, sender: "user" }])
  }

  // const { completion, setInput, handleSubmit } = useCompletion({
  //   api: "http://127.0.0.1:8000/chat-stream/",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  //   onResponse: res => {
  //     console.log("something happened");
  //   },
  //   onFinish: () => {
  //     console.log("something happened");
  //   },
  // });

  // const sendMessage = async (message: string) => {
  //   // setInput({
  //   //   current_url: window.location.href,
  //   //   history: messages,
  //   //   query: message
  //   // })
  //   setMessages((messages) => [...messages, { message, sender: "user" }])

  //   const syntheticEvent = {
  //     preventDefault: () => {},
  //     stopPropagation: () => {},
  //   } as React.FormEvent<HTMLFormElement>;
    
  //   await handleSubmit(syntheticEvent);

  //   setMessages((messages) => [
  //     ...messages,
  //     { message: completion, sender: "bot" }
  //   ])
  // }

  return (
    <div className="max-h-screen overflow-y-auto">
      <div className="flex-1 overflow-y-auto max-h-[80vh]">
        {messages.map((chatMessage, index) => (
          <div key={index}>
            <div className="p-3">
              <ChatMessage
                {...chatMessage}
                showPopularQuestions={showPopularQuestions}
                sendMessage={sendMessage}
              />
            </div>
            {index < messages.length - 1 && <Separator />}
          </div>
        ))}
      </div>
      <div className="p-4 px-10">
        <PromptForm sendMessage={sendMessage} />
      </div>
    </div>
  )
}

export default Chat


  // const sendMessage = async (message: string) => {
  //   setMessages((messages) => [...messages, { message, sender: "user" }])

  //   const response = await chatSendMessageStream({
  //     current_url: window.location.href,
  //     history: messages,
  //     query: message
  //   })

  //   console.log("Repsonse: ", response);

  //   // setMessages((messages) => [
  //   //   ...messages,
  //   //   { message: response.answer, sender: "bot" }
  //   // ])
  // }
