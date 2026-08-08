import React, { useState, useEffect } from 'react';
import api from '../api';
import { ShieldCheck, Lock, UserCheck, CheckCircle2, AlertCircle } from 'lucide-react';

export const RbacAdmin = () => {
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [targetUserId, setTargetUserId] = useState('');
  const [selectedRole, setSelectedRole] = useState('User');
  const [msg, setMsg] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [rRes, pRes] = await Promise.all([
        api.get('/rbac/roles'),
        api.get('/rbac/permissions')
      ]);
      setRoles(rRes.data);
      setPermissions(pRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAssignRole = async (e) => {
    e.preventDefault();
    setMsg(null);
    setError(null);
    try {
      const res = await api.post('/rbac/assign-role', {
        user_id: targetUserId,
        role_name: selectedRole
      });
      setMsg(res.data.message);
    } catch (err) {
      setError(err.response?.data?.message || 'Role assignment failed.');
    }
  };

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }} className="animate-fade-in">
      <div className="glass-card" style={{ padding: '24px 32px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '800', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <ShieldCheck size={22} color="#6366f1" /> Granular Role-Based Access Control (RBAC)
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginTop: '2px' }}>
          Declarative roles, permission matrices, and dynamic permission resolution
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
        {/* Assign Role Panel */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <UserCheck size={18} color="#10b981" /> Assign Role to User
          </h3>

          {msg && (
            <div style={{ padding: '10px 12px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '8px', color: '#34d399', fontSize: '12px', marginBottom: '12px', display: 'flex', gap: '6px' }}>
              <CheckCircle2 size={16} /> {msg}
            </div>
          )}

          {error && (
            <div style={{ padding: '10px 12px', background: 'rgba(244, 63, 94, 0.1)', border: '1px solid rgba(244, 63, 94, 0.3)', borderRadius: '8px', color: '#fb7185', fontSize: '12px', marginBottom: '12px', display: 'flex', gap: '6px' }}>
              <AlertCircle size={16} /> {error}
            </div>
          )}

          <form onSubmit={handleAssignRole} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '6px' }}>Target User UUID</label>
              <input
                type="text"
                required
                className="input-field"
                placeholder="Target UUID string"
                value={targetUserId}
                onChange={(e) => setTargetUserId(e.target.value)}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: 'var(--text-muted)', marginBottom: '6px' }}>Select System Role</label>
              <select
                className="input-field"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                style={{ background: 'rgba(15, 23, 42, 0.9)' }}
              >
                <option value="User">User (Standard Access)</option>
                <option value="Admin">Admin (Full System Privilege)</option>
                <option value="Auditor">Auditor (Audit Log Access)</option>
              </select>
            </div>

            <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: '4px' }}>
              Assign Role Now
            </button>
          </form>
        </div>

        {/* Roles Matrix */}
        <div className="glass-card" style={{ padding: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Lock size={18} color="#f59e0b" /> Configured Roles & Permissions
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {roles.map((r) => (
              <div key={r.id} style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontWeight: '700', fontSize: '14px', color: '#818cf8' }}>{r.name}</span>
                  <span className="badge badge-indigo">{r.permissions.length} perms</span>
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '8px' }}>{r.description}</div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {r.permissions.map((p) => (
                    <code key={p.id} style={{ fontSize: '11px', background: 'rgba(99, 102, 241, 0.1)', color: '#34d399', padding: '2px 8px', borderRadius: '4px', border: '1px solid rgba(99, 102, 241, 0.2)' }}>
                      {p.code}
                    </code>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
