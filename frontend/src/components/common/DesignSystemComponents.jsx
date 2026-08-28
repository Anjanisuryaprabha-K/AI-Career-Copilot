import React, { useState, useEffect } from 'react';

/**
 * Score Semantics Badge
 * Mappings:
 * 90-100: Excellent (#059669)
 * 75-89: Good (#10B981)
 * 50-74: Needs Improvement (#D97706)
 * 0-49: Needs Attention (#DC2626)
 */
export const ScoreBadge = ({ score, showLabel = true, size = 'md' }) => {
  const num = typeof score === 'number' ? score : parseFloat(score) || 0;
  
  let label = 'Needs Attention';
  let badgeStyle = 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20';
  let dotStyle = 'bg-rose-500';

  if (num >= 90) {
    label = 'Excellent';
    badgeStyle = 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20';
    dotStyle = 'bg-emerald-500';
  } else if (num >= 75) {
    label = 'Good';
    badgeStyle = 'bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20';
    dotStyle = 'bg-teal-500';
  } else if (num >= 50) {
    label = 'Needs Improvement';
    badgeStyle = 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
    dotStyle = 'bg-amber-500';
  }

  const sizeClasses = size === 'sm' 
    ? 'text-[11px] px-2 py-0.5 gap-1.5'
    : size === 'lg'
    ? 'text-sm px-3 py-1 gap-2'
    : 'text-xs px-2.5 py-1 gap-1.5';

  return (
    <span className={`inline-flex items-center font-semibold rounded-full border ${badgeStyle} ${sizeClasses}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${dotStyle}`} />
      <span>{num}%</span>
      {showLabel && <span className="opacity-80 font-normal">({label})</span>}
    </span>
  );
};

/**
 * Reusable AI Insight Component (#F5F3FF bg, #DDD6FE border, #7C3AED icon)
 */
export const AIInsightCard = ({ title = 'AI Insight', children, icon = '✨', className = '' }) => {
  return (
    <div className={`ai-insight-card p-5 relative overflow-hidden ${className}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-[#7C3AED]/10 text-[#7C3AED] dark:text-[#8B5CF6] border border-[#DDD6FE] dark:border-[#3B2D54]">
          <span>{icon}</span>
          <span>{title}</span>
        </span>
      </div>
      <div className="text-slate-800 dark:text-slate-200 text-sm leading-relaxed">
        {children}
      </div>
    </div>
  );
};

/**
 * Animated Count-Up Number
 */
export const AnimatedNumber = ({ value = 0, duration = 1000, suffix = '', prefix = '' }) => {
  const [displayValue, setDisplayValue] = useState(0);
  const target = typeof value === 'number' ? value : parseFloat(value) || 0;

  useEffect(() => {
    // Check reduced motion preference
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setDisplayValue(target);
      return;
    }

    let start = 0;
    const startTime = performance.now();

    const updateCounter = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(start + (target - start) * easeProgress);

      setDisplayValue(current);

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      }
    };

    requestAnimationFrame(updateCounter);
  }, [target, duration]);

  return <span>{prefix}{displayValue}{suffix}</span>;
};

/**
 * Animated Progress Bar with Indigo default
 */
export const AnimatedProgressBar = ({ value = 0, height = 'h-2.5', showSemanticColor = false, className = '' }) => {
  const [width, setWidth] = useState(0);
  const target = Math.min(100, Math.max(0, typeof value === 'number' ? value : parseFloat(value) || 0));

  useEffect(() => {
    const timer = setTimeout(() => {
      setWidth(target);
    }, 50);
    return () => clearTimeout(timer);
  }, [target]);

  let barColor = 'bg-[#4F46E5] dark:bg-[#6366F1]';
  if (showSemanticColor) {
    if (target >= 90) barColor = 'bg-[#059669]';
    else if (target >= 75) barColor = 'bg-[#10B981]';
    else if (target >= 50) barColor = 'bg-[#D97706]';
    else barColor = 'bg-[#DC2626]';
  }

  return (
    <div className={`w-full bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden ${height} ${className}`}>
      <div 
        className={`${height} ${barColor} rounded-full transition-all duration-1000 ease-out`}
        style={{ width: `${width}%` }}
      />
    </div>
  );
};

/**
 * Skeleton Loader Component
 */
export const SkeletonCard = ({ rows = 3, className = '' }) => {
  return (
    <div className={`prof-card p-6 space-y-4 ${className}`}>
      <div className="skeleton-pulse h-6 w-1/3" />
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="skeleton-pulse h-4 w-full" style={{ width: `${100 - i * 15}%` }} />
      ))}
    </div>
  );
};

export const SkeletonTable = ({ rows = 5, cols = 4 }) => {
  return (
    <div className="prof-card overflow-hidden">
      <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex justify-between">
        <div className="skeleton-pulse h-5 w-40" />
        <div className="skeleton-pulse h-5 w-24" />
      </div>
      <div className="p-4 space-y-3">
        {Array.from({ length: rows }).map((_, r) => (
          <div key={r} className="flex items-center gap-4">
            {Array.from({ length: cols }).map((_, c) => (
              <div key={c} className="skeleton-pulse h-4 flex-1" />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

/**
 * Empty State Banner
 */
export const EmptyState = ({ 
  title = 'No data available', 
  description = 'Complete your first activity to start generating insights.',
  icon = '📊',
  actionLabel,
  onAction
}) => {
  return (
    <div className="prof-card p-10 text-center flex flex-col items-center justify-center max-w-lg mx-auto my-8">
      <div className="w-16 h-16 rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-100 dark:border-indigo-800 flex items-center justify-center text-3xl mb-4 shadow-xs">
        {icon}
      </div>
      <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-1">{title}</h3>
      <p className="text-sm text-slate-500 dark:text-slate-400 mb-6 max-w-sm">{description}</p>
      {actionLabel && onAction && (
        <button onClick={onAction} className="btn-primary">
          {actionLabel}
        </button>
      )}
    </div>
  );
};

/**
 * Unified Page Header with Indigo & Violet styling
 */
export const PageHeader = ({ title, subtitle, category, badgeText, actions }) => {
  return (
    <div className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 dark:border-slate-800/80 pb-5">
      <div>
        {category && (
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#4F46E5] dark:text-[#818CF8] mb-1">
            <span>{category}</span>
            {badgeText && (
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-[#7C3AED]/10 text-[#7C3AED] dark:text-[#8B5CF6] border border-[#DDD6FE] dark:border-[#3B2D54]">
                {badgeText}
              </span>
            )}
          </div>
        )}
        <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">
          {title}
        </h1>
        {subtitle && (
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
            {subtitle}
          </p>
        )}
      </div>
      {actions && (
        <div className="flex items-center gap-3 shrink-0">
          {actions}
        </div>
      )}
    </div>
  );
};
