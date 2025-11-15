import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { XMarkIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';

interface PrivacyPolicyModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PrivacyPolicyModal = ({ isOpen, onClose }: PrivacyPolicyModalProps) => {
  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-3xl transform overflow-hidden rounded-2xl bg-white dark:bg-gray-800 shadow-2xl transition-all">
                {/* Header */}
                <div className="flex items-center justify-between border-b border-gray-200 dark:border-gray-700 px-6 py-4 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                      <ShieldCheckIcon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <Dialog.Title className="text-xl font-bold text-gray-900 dark:text-white">
                      Privacy Policy & Terms of Service
                    </Dialog.Title>
                  </div>
                  <button
                    onClick={onClose}
                    className="p-2 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                </div>

                {/* Content */}
                <div className="px-6 py-6 max-h-[70vh] overflow-y-auto custom-scrollbar">
                  <div className="prose prose-sm dark:prose-invert max-w-none space-y-6">
                    
                    {/* Last Updated */}
                    <p className="text-sm text-gray-500 dark:text-gray-400 italic">
                      Last Updated: November 15, 2025
                    </p>

                    {/* Introduction */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        1. Introduction
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        Welcome to <span className="font-semibold text-blue-600 dark:text-blue-400">CareerStar</span> (also referred to as "Utopia", "we", "our", or "us"). 
                        We are committed to protecting your privacy and ensuring transparency about how we collect, use, and protect your personal information.
                      </p>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed mt-2">
                        By creating an account and using our services, you agree to the collection and use of information in accordance with this policy.
                      </p>
                    </section>

                    {/* Data Collection */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        2. Information We Collect
                      </h3>
                      <div className="space-y-3">
                        <div>
                          <h4 className="font-semibold text-gray-800 dark:text-gray-200">2.1 Personal Information</h4>
                          <ul className="list-disc list-inside ml-4 mt-2 space-y-1 text-gray-700 dark:text-gray-300">
                            <li>Full name and email address</li>
                            <li>Account credentials (encrypted passwords)</li>
                            <li>Profile information you choose to provide</li>
                          </ul>
                        </div>
                        
                        <div>
                          <h4 className="font-semibold text-gray-800 dark:text-gray-200">2.2 Professional Information</h4>
                          <ul className="list-disc list-inside ml-4 mt-2 space-y-1 text-gray-700 dark:text-gray-300">
                            <li>Resume/CV data (skills, experience, education)</li>
                            <li>Job preferences and search history</li>
                            <li>Interview responses and performance data</li>
                            <li>Career footprint and activity tracking</li>
                          </ul>
                        </div>

                        <div>
                          <h4 className="font-semibold text-gray-800 dark:text-gray-200">2.3 Usage Data</h4>
                          <ul className="list-disc list-inside ml-4 mt-2 space-y-1 text-gray-700 dark:text-gray-300">
                            <li>Application usage patterns and interactions</li>
                            <li>Feature engagement metrics</li>
                            <li>Technical data (IP address, browser type, device information)</li>
                          </ul>
                        </div>
                      </div>
                    </section>

                    {/* How We Use Your Data */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        3. How We Use Your Information
                      </h3>
                      <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 p-4 rounded-r-lg">
                        <p className="text-gray-800 dark:text-gray-200 font-medium mb-2">
                          ⚠️ Important: AI Model Training
                        </p>
                        <p className="text-gray-700 dark:text-gray-300 text-sm">
                          Your data will be used to train and improve our AI/ML models to provide better recommendations, 
                          resume analysis, interview simulations, and job matching services.
                        </p>
                      </div>
                      
                      <ul className="list-disc list-inside ml-4 mt-4 space-y-2 text-gray-700 dark:text-gray-300">
                        <li><strong>Service Provision:</strong> To provide and maintain our career services platform</li>
                        <li><strong>Personalization:</strong> To customize your experience and provide tailored recommendations</li>
                        <li><strong>AI Model Training:</strong> To train, test, and improve our machine learning algorithms</li>
                        <li><strong>Analytics:</strong> To analyze usage patterns and improve our services</li>
                        <li><strong>Communication:</strong> To send you updates, notifications, and support messages</li>
                        <li><strong>Security:</strong> To detect, prevent, and address technical issues and fraud</li>
                      </ul>
                    </section>

                    {/* Data Sharing */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        4. Data Sharing and Disclosure
                      </h3>
                      <div className="space-y-3 text-gray-700 dark:text-gray-300">
                        <p>We may share your information in the following circumstances:</p>
                        <ul className="list-disc list-inside ml-4 space-y-1">
                          <li><strong>With Your Consent:</strong> When you explicitly authorize us to share specific information</li>
                          <li><strong>Service Providers:</strong> With third-party vendors who assist in operating our platform (e.g., cloud hosting, AI services)</li>
                          <li><strong>Aggregated Data:</strong> Non-identifiable, anonymized data for research and analytics</li>
                          <li><strong>Legal Requirements:</strong> When required by law or to protect our legal rights</li>
                        </ul>
                        <div className="mt-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                          <p className="text-sm text-green-800 dark:text-green-300">
                            ✓ We will <strong>never</strong> sell your personal information to third parties.
                          </p>
                        </div>
                      </div>
                    </section>

                    {/* Data Security */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        5. Data Security
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        We implement industry-standard security measures to protect your data:
                      </p>
                      <ul className="list-disc list-inside ml-4 mt-2 space-y-1 text-gray-700 dark:text-gray-300">
                        <li>Encrypted password storage using secure hashing algorithms</li>
                        <li>Secure HTTPS connections for all data transmission</li>
                        <li>Regular security audits and updates</li>
                        <li>Access controls and authentication mechanisms</li>
                      </ul>
                    </section>

                    {/* Your Rights */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        6. Your Rights
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 mb-2">You have the right to:</p>
                      <ul className="list-disc list-inside ml-4 space-y-1 text-gray-700 dark:text-gray-300">
                        <li><strong>Access:</strong> Request a copy of your personal data</li>
                        <li><strong>Correction:</strong> Update or correct inaccurate information</li>
                        <li><strong>Deletion:</strong> Request deletion of your account and associated data</li>
                        <li><strong>Portability:</strong> Export your data in a machine-readable format</li>
                        <li><strong>Opt-out:</strong> Withdraw consent for AI model training (may limit service features)</li>
                      </ul>
                    </section>

                    {/* Data Retention */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        7. Data Retention
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        We retain your personal information for as long as your account is active or as needed to provide services. 
                        After account deletion, anonymized data may be retained for AI model training and analytics purposes.
                      </p>
                    </section>

                    {/* Cookies */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        8. Cookies and Tracking
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        We use cookies and similar technologies to maintain your session, remember preferences, and analyze usage patterns. 
                        You can control cookie settings through your browser preferences.
                      </p>
                    </section>

                    {/* Children's Privacy */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        9. Children's Privacy
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        Our services are not intended for individuals under 16 years of age. We do not knowingly collect 
                        personal information from children.
                      </p>
                    </section>

                    {/* Changes to Policy */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        10. Changes to This Policy
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        We may update this privacy policy periodically. We will notify you of significant changes via email 
                        or through a prominent notice on our platform.
                      </p>
                    </section>

                    {/* Contact */}
                    <section>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                        11. Contact Us
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                        If you have questions about this Privacy Policy or wish to exercise your rights, please contact us at:
                      </p>
                      <div className="mt-3 p-4 bg-gray-50 dark:bg-gray-900/50 rounded-lg">
                        <p className="text-gray-800 dark:text-gray-200">
                          <strong>Email:</strong> privacy@careerstar.com<br />
                          <strong>Address:</strong> CareerStar/Utopia Privacy Team<br />
                          <strong>Response Time:</strong> Within 30 days
                        </p>
                      </div>
                    </section>

                  </div>
                </div>

                {/* Footer */}
                <div className="border-t border-gray-200 dark:border-gray-700 px-6 py-4 bg-gray-50 dark:bg-gray-900/50">
                  <button
                    onClick={onClose}
                    className="w-full sm:w-auto px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors shadow-md hover:shadow-lg"
                  >
                    Close
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
};
