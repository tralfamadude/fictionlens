"use client";

import { useChat } from "ai/react";
import { useMemo } from "react";
import { insertDataIntoMessages } from "../components/transform";
import Image from 'next/image';
import image from "./gatsby_sentiment.png";

export default function StorySection() {
    const {
        messages,
        input,
        isLoading,
        handleSubmit,
        handleInputChange,
        reload,
        stop,
        data,
    } = useChat({
        api: process.env.NEXT_PUBLIC_CHAT_API,
        headers: {
            "Content-Type": "application/json", // using JSON because of vercel/ai 2.2.26
        },
    });

    const transformedMessages = useMemo(() => {
        return insertDataIntoMessages(messages, data);
    }, [messages, data]);

    return (
        <div className="space-y-4 max-w-5xl w-full">
            <Image
                src={image}
                alt="logo"
                width={1000}
                height={1000}
                loading="lazy"
            />
        </div>
    );
}
