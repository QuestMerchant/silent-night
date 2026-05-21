const roleDetailsByKey = {
  civilian: {
    title: 'Civilian',
    description: 'Find and eliminate the Serial Killer. During the day, vote with the group.',
    image: '/nosy%20neighbor.jpeg'
  },
  spy: {
    title: 'Spy',
    description: 'At night, you may investigate a player to learn their role.',
    image: '/spy.jpeg'
  },
  serial_killer: {
    title: 'Serial Killer',
    description: 'At night, work with other killers to eliminate a player. Win by outnumbering the town.',
    image: '/killer.jpeg'
  },
  detective: {
    title: 'Detective',
    description: 'Investigate players and help the town identify the killer.',
    image: '/detective.jpeg'
  }
}

function normalizeRoleKey(roleNameOrKey) {
  if (!roleNameOrKey) return ''

  const raw = String(roleNameOrKey).trim()
  if (!raw) return ''

  const lower = raw.toLowerCase()

  // Backend uses these role names today (see backend/game.py)
  if (lower === 'civilian') return 'civilian'
  if (lower === 'spy' || lower === 'spies') return 'spy'
  if (lower === 'serial killer' || lower === 'serial killers') return 'serial_killer'

  // If we get an already-normalized key
  if (roleDetailsByKey[lower]) return lower

  // Try a safe normalization fallback
  return lower
    .replace(/\s+/g, '_')
    .replace(/[^a-z0-9_]/g, '')
}

export function getRoleDetails(roleNameOrKey) {
  const key = normalizeRoleKey(roleNameOrKey)
  return (
    roleDetailsByKey[key] ?? {
      title: roleNameOrKey ? String(roleNameOrKey) : 'Unknown role',
      description: 'Role details not found.',
      image: '/Silent%20Night.png'
    }
  )
}

