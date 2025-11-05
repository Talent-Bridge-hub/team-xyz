/**
 * Resume Templates Modal Component
 * Displays available resume templates for users to download
 */

import { useState, useEffect } from 'react';
import { resumeService } from '../../services/resume.service';
import { useToast } from '../../contexts/ToastContext';

interface Template {
  id: string;
  name: string;
  description: string;
  best_for: string;
  ats_friendly: boolean;
  sections: string[];
}

interface ResumeTemplatesModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ResumeTemplatesModal({ isOpen, onClose }: ResumeTemplatesModalProps) {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const { showSuccess, showError } = useToast();

  useEffect(() => {
    if (isOpen) {
      loadTemplates();
    }
  }, [isOpen]);

  const loadTemplates = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await resumeService.listTemplates();
      setTemplates(response.templates || []);
    } catch (err: any) {
      console.error('Failed to load templates:', err);
      setError('Failed to load templates. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadTemplate = async (templateId: string, templateName: string) => {
    try {
      setError('');
      const blob = await resumeService.downloadTemplate(templateId);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `resume_template_${templateName.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      // Show success message
      showSuccess(`Template "${templateName}" downloaded successfully! Fill in your details, save it, and upload it for analysis.`);
      
    } catch (err: any) {
      console.error('Download failed:', err);
      const errorMsg = `Failed to download template: ${err.message}`;
      setError(errorMsg);
      showError(errorMsg);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="relative bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Resume Templates</h2>
              <p className="text-sm text-gray-600 mt-1">Choose a professional template to get started</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition"
            >
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-6">
            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : error ? (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-1">
                {templates.map((template) => (
                  <div
                    key={template.id}
                    className="border border-gray-200 rounded-lg p-6 hover:border-blue-400 hover:shadow-md transition"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-xl font-semibold text-gray-900">{template.name}</h3>
                          {template.ats_friendly && (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              ✓ ATS-Friendly
                            </span>
                          )}
                        </div>
                        
                        <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                        
                        <div className="flex items-center space-x-4 text-sm mb-4">
                          <div className="flex items-center text-blue-600">
                            <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            <span className="font-medium">{template.best_for}</span>
                          </div>
                        </div>

                        <div className="mb-4">
                          <p className="text-xs font-medium text-gray-700 mb-2">Includes Sections:</p>
                          <div className="flex flex-wrap gap-2">
                            {template.sections.map((section, idx) => (
                              <span
                                key={idx}
                                className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700"
                              >
                                {section}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => handleDownloadTemplate(template.id, template.name)}
                        className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition flex items-center space-x-2 whitespace-nowrap"
                      >
                        <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        <span>Download</span>
                      </button>
                    </div>

                    {/* Preview/Details */}
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <details className="text-sm">
                        <summary className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium">
                          View Template Details
                        </summary>
                        <div className="mt-3 text-gray-600 space-y-2">
                          <p><strong>Best For:</strong> {template.best_for}</p>
                          <p><strong>Format:</strong> DOCX (editable Word document)</p>
                          <p><strong>ATS Compatible:</strong> {template.ats_friendly ? 'Yes - Passes applicant tracking systems' : 'No'}</p>
                          <p className="text-xs text-gray-500 mt-2">
                            💡 <strong>Tip:</strong> Download the template, edit it in Word/Google Docs, save as PDF, then upload it here for analysis and scoring!
                          </p>
                        </div>
                      </details>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Info Box */}
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
              <h4 className="text-sm font-medium text-blue-900 mb-2">How to Use Templates</h4>
              <ol className="text-xs text-blue-800 space-y-1 list-decimal list-inside">
                <li>Click "Download" on your preferred template</li>
                <li>Open the DOCX file in Microsoft Word, Google Docs, or LibreOffice</li>
                <li>Replace placeholder text with your actual experience, skills, and education</li>
                <li>Save the completed resume as a PDF</li>
                <li>Upload it using the "Upload Resume" button for AI analysis and scoring</li>
              </ol>
            </div>
          </div>

          {/* Footer */}
          <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
