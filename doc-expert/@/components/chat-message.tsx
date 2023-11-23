import { cn } from "@/lib/utils"
import { PersonIcon } from "@radix-ui/react-icons"
import Markdown from "markdown-to-jsx"
import { CopyBlock, dracula } from "react-code-blocks"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { oneLight as CodeStyle } from "react-syntax-highlighter/dist/esm/styles/prism"
import showdown from "showdown"

import type { ChatMessageSchema } from "~api/openapi/schemas"

import { Button } from "./ui/button"

const CustomPre = ({ children, ...props }) => {
  console.log("children " + children)
  console.log("props " + props)
  return (
    <div className="rounded-sm">
      <div className="flex items-center text-sm rounded-t-md bg-foreground/70 text-background">
        <div className="flex p-1 ml-2">
          <span>python</span>
        </div>
        <div className="flex-1"></div>
      </div>
      <div className="p-3">{children}</div>
    </div>
  )
}

const CustomCodeBlock = ({ className, children }) => {
  if (className === undefined) {
    return (
      <code className="bg-[#9593fa] p-1 text-xs font-semibold">{children}</code>
    )
  }
  let lang = "text"
  if (className && className.startsWith("lang-")) {
    lang = className.replace("lang-", "")
  }
  return (
    <div>
      <SyntaxHighlighter
        language={lang}
        style={CodeStyle}
        PreTag={CustomPre}
        codeTagProps="">
        {children}
      </SyntaxHighlighter>
    </div>
  )
}

type ChatMessageProps = {
  showPopularQuestions?: boolean
  sendMessage?: (message: string) => void
} & ChatMessageSchema

const ChatMessage = ({
  message,
  sender,
  showPopularQuestions = false,
  sendMessage
}: ChatMessageProps) => {
  const questions = [
    "How do I get started with using the Airbyte API?",
    "What are the steps to set up a source in Airbyte Cloud?",
    "How can I deploy and manage Airbyte Open Source in my cloud infrastructure?"
  ]
  const converter = new showdown.Converter()
  const html = converter.makeHtml(message)
  const icon =
    sender === "bot" ? (
      <img
        src="https://cf.appdrag.com/dashboard-openvm-clo-b2d42c/uploads/airbyte-1613152137-dKaX.png"
        alt="Airbyte Logo"
      />
    ) : (
      <PersonIcon className="w-5 h-5" />
    )
  return (
    <div className={cn("mb-2 flex")}>
      <div
        className={cn(
          "flex h-6 w-6 shrink-0 select-none items-center justify-center rounded-md"
        )}>
        {icon}
      </div>

      <div className="flex-1 px-1 ml-4 space-y-2 overflow-hidden">
        <Markdown
          options={{
            overrides: {
              p: {
                component: "div",
                props: {
                  className: "text-md"
                }
              },
              code: {
                component: CustomCodeBlock
              },
              pre: {
                component: "pre",
                props: {
                  className: "p-0"
                }
              }
            }
          }}>
          {message}
        </Markdown>
        {showPopularQuestions && (
          <div className="pt-4">
            <div className="text-xs font-semibold text-foreground/60 uppercase tracking-widest py-2">
              Popular Questions
            </div>
            <div className="flex flex-wrap">
              {questions.map((question) => (
                <Button
                  variant="outline"
                  className="mb-2"
                  key={question}
                  onClick={() => {
                    sendMessage(question)
                  }}>
                  {question}
                </Button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatMessage
