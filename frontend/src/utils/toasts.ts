import { toast } from 'vue-sonner';
import './toasts.css';


export const showExperimentsToast = () => {
    toast.error('Navigation Error', {
        description: 'Unable to navigate to Brain Dump. If this issue continues, please contact support.',
        duration: 3000,
        position: 'bottom-right',
        style: {
            background: 'var(--element-color-1)',
            color: 'var(--light-text)',
            border: '1px solid var(--highlight-color)',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        },
    });
};

export const showSignupToast = (userEmail: string) => {
    toast.success('Account Created Successfully', {
        description: `We just sent an email to ${userEmail}. Please check your inbox and click the link.`,
        duration: Infinity,
        position: 'top-center',
        class: 'signup-toast',
    });
};
