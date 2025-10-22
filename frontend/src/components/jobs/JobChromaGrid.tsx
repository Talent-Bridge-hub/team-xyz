import React, { useRef, useEffect } from 'react';
import { gsap } from 'gsap';
import { JobPost } from '../../services/jobs.service';
import './JobChromaGrid.css';

export interface JobChromaGridProps {
  jobs: JobPost[];
  className?: string;
  radius?: number;
  columns?: number;
  damping?: number;
  fadeOut?: number;
  ease?: string;
  onJobClick?: (job: JobPost) => void;
}

type SetterFn = (v: number | string) => void;

const JobChromaGrid: React.FC<JobChromaGridProps> = ({
  jobs,
  className = '',
  radius = 300,
  columns = 3,
  damping = 0.45,
  fadeOut = 0.6,
  ease = 'power3.out',
  onJobClick
}) => {
  const rootRef = useRef<HTMLDivElement>(null);
  const fadeRef = useRef<HTMLDivElement>(null);
  const setX = useRef<SetterFn | null>(null);
  const setY = useRef<SetterFn | null>(null);
  const pos = useRef({ x: 0, y: 0 });

  // Color palette for different job categories (matching frontend theme)
  const colorPalette = [
    { border: '#3B82F6', gradient: 'linear-gradient(145deg, #1E40AF 0%, #1F2937 100%)' }, // Blue
    { border: '#10B981', gradient: 'linear-gradient(210deg, #059669 0%, #1F2937 100%)' }, // Green
    { border: '#F59E0B', gradient: 'linear-gradient(165deg, #D97706 0%, #1F2937 100%)' }, // Amber
    { border: '#EF4444', gradient: 'linear-gradient(195deg, #DC2626 0%, #1F2937 100%)' }, // Red
    { border: '#8B5CF6', gradient: 'linear-gradient(225deg, #7C3AED 0%, #1F2937 100%)' }, // Purple
    { border: '#06B6D4', gradient: 'linear-gradient(135deg, #0891B2 0%, #1F2937 100%)' }, // Cyan
  ];

  useEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    setX.current = gsap.quickSetter(el, '--x', 'px') as SetterFn;
    setY.current = gsap.quickSetter(el, '--y', 'px') as SetterFn;
    const { width, height } = el.getBoundingClientRect();
    pos.current = { x: width / 2, y: height / 2 };
    setX.current(pos.current.x);
    setY.current(pos.current.y);
  }, []);

  const moveTo = (x: number, y: number) => {
    gsap.to(pos.current, {
      x,
      y,
      duration: damping,
      ease,
      onUpdate: () => {
        setX.current?.(pos.current.x);
        setY.current?.(pos.current.y);
      },
      overwrite: true
    });
  };

  const handleMove = (e: React.PointerEvent) => {
    const r = rootRef.current!.getBoundingClientRect();
    moveTo(e.clientX - r.left, e.clientY - r.top);
    gsap.to(fadeRef.current, { opacity: 0, duration: 0.25, overwrite: true });
  };

  const handleLeave = () => {
    gsap.to(fadeRef.current, {
      opacity: 1,
      duration: fadeOut,
      overwrite: true
    });
  };

  const handleCardClick = (job: JobPost) => {
    if (onJobClick) {
      onJobClick(job);
    } else if (job.url) {
      window.open(job.url, '_blank', 'noopener,noreferrer');
    }
  };

  const handleApplyClick = (e: React.MouseEvent, job: JobPost) => {
    e.stopPropagation(); // Prevent card click from firing
    
    if (job.url) {
      window.open(job.url, '_blank', 'noopener,noreferrer');
    } else {
      // Fallback: trigger the onJobClick if no URL is available
      if (onJobClick) {
        onJobClick(job);
      }
    }
  };

  const handleCardMove: React.MouseEventHandler<HTMLElement> = e => {
    const card = e.currentTarget as HTMLElement;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.setProperty('--mouse-x', `${x}px`);
    card.style.setProperty('--mouse-y', `${y}px`);
  };

  const getJobColor = (index: number) => {
    return colorPalette[index % colorPalette.length];
  };

  const formatSalary = (job: JobPost) => {
    if (!job.salary_range) return null;
    const { min, max, currency = 'USD' } = job.salary_range;
    if (min && max) {
      return `${currency} ${(min / 1000).toFixed(0)}k - ${(max / 1000).toFixed(0)}k`;
    } else if (min) {
      return `From ${currency} ${(min / 1000).toFixed(0)}k`;
    } else if (max) {
      return `Up to ${currency} ${(max / 1000).toFixed(0)}k`;
    }
    return null;
  };

  return (
    <div
      ref={rootRef}
      className={`job-chroma-grid ${className}`}
      style={
        {
          '--r': `${radius}px`,
          '--cols': columns,
        } as React.CSSProperties
      }
      onPointerMove={handleMove}
      onPointerLeave={handleLeave}
    >
      {jobs.map((job, i) => {
        const colors = getJobColor(i);
        const salary = formatSalary(job);
        
        return (
          <article
            key={job.id}
            className="job-chroma-card"
            onMouseMove={handleCardMove}
            onClick={() => handleCardClick(job)}
            style={
              {
                '--card-border': colors.border,
                '--card-gradient': colors.gradient,
                cursor: 'pointer'
              } as React.CSSProperties
            }
          >
            {/* Job Icon/Logo Placeholder */}
            <div className="job-icon-wrapper">
              <div className="job-icon">
                <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" 
                  />
                </svg>
              </div>
            </div>

            {/* Job Info */}
            <footer className="job-chroma-info">
              <div className="job-header">
                <h3 className="job-title">{job.title}</h3>
                <p className="job-company">{job.company}</p>
              </div>

              <div className="job-details">
                <div className="job-location">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span>{job.location}</span>
                </div>

                {job.experience_level && (
                  <div className="job-badge job-experience">
                    {job.experience_level}
                  </div>
                )}

                {job.remote && (
                  <div className="job-badge job-remote">
                    🏠 Remote
                  </div>
                )}
              </div>

              {salary && (
                <div className="job-salary">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{salary}</span>
                </div>
              )}

              {job.required_skills && job.required_skills.length > 0 && (
                <div className="job-skills">
                  {job.required_skills.slice(0, 3).map((skill, idx) => (
                    <span key={idx} className="skill-tag">
                      {skill}
                    </span>
                  ))}
                  {job.required_skills.length > 3 && (
                    <span className="skill-count">
                      +{job.required_skills.length - 3}
                    </span>
                  )}
                </div>
              )}

              <div className="job-footer">
                <span className="job-type">{job.type}</span>
                <button 
                  className="apply-btn"
                  onClick={(e) => handleApplyClick(e, job)}
                  aria-label={`Apply for ${job.title} at ${job.company}`}
                >
                  Apply Now →
                </button>
              </div>
            </footer>
          </article>
        );
      })}
      <div className="chroma-overlay" />
      <div ref={fadeRef} className="chroma-fade" />
    </div>
  );
};

export default JobChromaGrid;
