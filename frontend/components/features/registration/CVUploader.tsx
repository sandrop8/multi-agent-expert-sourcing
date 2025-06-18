import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useRef } from "react";

interface CVUploaderProps {
    selectedFile: File | null;
    onFileSelect: (file: File | null) => void;
    onUpload: () => void;
    isUploading?: boolean;
    uploadStatus?: string;
    currentStatus?: {
        status: string;
        message: string;
        progress: number;
    } | null;
}

export default function CVUploader({
    selectedFile,
    onFileSelect,
    onUpload,
    isUploading = false,
    uploadStatus = "",
    currentStatus = null
}: CVUploaderProps) {
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            // Check file type
            const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (!allowedTypes.includes(file.type)) {
                onFileSelect(null);
                return;
            }
            // Check file size (10MB limit)
            if (file.size > 10 * 1024 * 1024) {
                onFileSelect(null);
                return;
            }
            onFileSelect(file);
        }
    };

    return (
        <div className="bg-muted/50 p-6 rounded-lg">
            <div className="space-y-4">
                <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center hover:border-muted-foreground/50 transition-colors">
                    <svg
                        className="w-12 h-12 mx-auto mb-4 text-muted-foreground"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                        />
                    </svg>

                    <Input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileSelect}
                        className="hidden"
                        id="cv-upload"
                    />

                    <label
                        htmlFor="cv-upload"
                        className="cursor-pointer"
                    >
                        <div className="text-sm text-muted-foreground">
                            <span className="text-primary hover:underline">
                                Click to upload CV (PDF or Word, max 10MB)
                            </span>
                        </div>
                    </label>
                </div>

                {selectedFile && (
                    <div className="text-sm text-muted-foreground">
                        Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                    </div>
                )}

                {(uploadStatus || currentStatus) && (
                    <div className="space-y-3">
                        {/* Progress Bar */}
                        {currentStatus && currentStatus.progress > 0 && (
                            <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className="bg-green-600 h-2 rounded-full transition-all duration-500 ease-out"
                                    style={{ width: `${currentStatus.progress}%` }}
                                ></div>
                            </div>
                        )}

                        {/* Status Message */}
                        <div className={`text-sm p-3 rounded ${currentStatus?.status === 'error' || uploadStatus.includes('failed') || uploadStatus.includes('error')
                                ? 'bg-red-100 text-red-700'
                                : 'bg-green-100 text-green-700'
                            }`}>
                            <div className="flex items-center space-x-2">
                                {/* Loading spinner for active processing */}
                                {isUploading && currentStatus?.status !== 'completed' && currentStatus?.status !== 'error' && (
                                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-green-600 border-t-transparent"></div>
                                )}
                                <span>{currentStatus?.message || uploadStatus}</span>
                            </div>
                        </div>
                    </div>
                )}

                <Button
                    onClick={onUpload}
                    disabled={!selectedFile || isUploading}
                    className="w-full"
                >
                    {isUploading ? "Uploading..." : "Upload CV"}
                </Button>
            </div>
        </div>
    );
}
