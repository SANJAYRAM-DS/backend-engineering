import React, { useState } from 'react';
import api from '../api';
import { MailCheck, KeyRound, CheckCircle2, AlertCircle } from 'lucide-react';

export const VerifyEmail = ({ setActiveTab }) => {
  const [token, setToken] = useState('');
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await api.post('/auth/verify-email', { token });
      setStatus(res.data.message);
    } catch (err) {
      setError(err.response?.data?.message || 'Verification failed. Token may be invalid or expired.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '440px', margin: '40px auto 0', padding: '0 16px' }} className="animate-fade-in">
      <div className="glass-card" style={{ padding: '36px 32px' }}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <div style={{ width: '48px', height: '48px', background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
            <MailCheck size={24} color="#10b981" />
          </div>
          <h2 style={{ fontSize: '22px', fontWeight: '700' }}>Email Verification</h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '4px' }}>
            Enter your cryptographic verification token
          </p>
        </div>

        {status ? (
          <div style={{ textAlign: 'center', padding: '20px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '12px' }}>
            <CheckCircle2 size={42} color="#10b981" style={{ margin: '0 auto 12px' }} />
            <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#34d399' }}>Email Verified!</h3>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)', margin: '8px 0 16px' }}>{status}</p>
            <button className="btn-primary" onClick={() => setActiveTab('login')} style={{ width: '100%' }}>
              Proceed to Login
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {error && (
              <div style={{ padding: '12px', background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', borderRadius: '10px', color: '#fb7185', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <AlertCircle size={18} /> {error}
              </div>
            )}

            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '6px' }}>Verification Token</label>
              <div style={{ position: 'relative' }}>
                <input
                  type="text"
                  required
                  className="input-field"
                  placeholder="Paste cryptographic token"
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  style={{ paddingLeft: '40px' }}
                />
                <KeyRound size={18} color="#6b7280" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
              </div>
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%' }}>
              {loading ? 'Verifying Token...' : 'Verify Email Address'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
