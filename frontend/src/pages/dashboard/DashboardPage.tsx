import { Routes, Route } from 'react-router-dom';
import { DashboardLayout } from '../../components/layout/DashboardLayout';
import { DashboardHome } from './DashboardHome';
import { ResumePage } from '../resume';
import JobsPage from '../jobs';
import InterviewPage from '../interview';
import FootprintPage from '../footprint/FootprintPage';

export const DashboardPage = () => {
  return (
    <DashboardLayout>
      <Routes>
        <Route path="/" element={<DashboardHome />} />
        <Route path="/resume" element={<ResumePage />} />
        <Route path="/jobs" element={<JobsPage />} />
        <Route path="/interview" element={<InterviewPage />} />
        <Route path="/footprint" element={<FootprintPage />} />
      </Routes>
    </DashboardLayout>
  );
};
