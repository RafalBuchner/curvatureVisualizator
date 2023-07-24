def solveCubicBezier(p1, p2, p3, p4):
	"""
	Solve cubic Bezier equation and 1st and 2nd derivative.
	"""
	ax = -p1x + 3.0 * p2x - 3.0 * p3x + p4x
	ay = -p1y + 3.0 * p2y - 3.0 * p3y + p4y
	a = (ax, ay)
	
	bx = 3.0 * p1x - 6.0 * p2x + 3.0 * p3x
	by = 3.0 * p1y - 6.0 * p2y + 3.0 * p3y
	b = (bx, by)
	
	cx = -3.0 * p1x + 3.0 * p2x
	cy = -3.0 * p1y + 3.0 * p2y
	c = (cx, cy)
	d = p1
	return a, b, c, d

def solveCubicBezierCurvature(a, b, c, d, t):
	"""
	Calc curvature using cubic Bezier equation and 1st and 2nd derivative.
	Returns position of on-curve point p1234, and vector of 1st and 2nd derivative.
	"""
	t3 = t**3
	t2 = t**2
	rx = ax*t3 + bx*t2 + cx*t + dx
	ry = ay*t3 + by*t2 + cy*t + dy
	r = (rx, ry)
	
	r1x = 3*ax*t2 + 2*bx*t + cx
	r1y = 3*ay*t2 + 2*by*t + cy
	r1 = (r1x, r1y)
	
	r2x = 6*ax*t + 2*bx
	r2y = 6*ay*t + 2*by
	r2 = (r2x, r2y)
	
	return (r, r1, r2, (r1x * r2y - r1y * r2x) / (r1x**2 + r1y**2)**1.5)


def getSegmentCurvatureBits(p1, p2, p3, p4):
	steps = int(max(TOTALSEGMENTS / self.speedpunklib.numberofcurvesegments, MINSEGMENTS - 1))
	
	curvatures = []
	a, b, c, d = solveCubicBezier(p1, p2, p3, p4)
	set2 = None
	for i in range(steps + 1):
		t = i / float(steps)
		
		curv = solveCubicBezierCurvature(a, b, c, d, t)
		curvatures.append(curv)

		# try:
		# 	set1 = solveCubicBezierCurvature(a, b, c, d, t)
		# 	if set2 is not None:
		# 		curvatures.append(Curvature(self, set1, set2))
		# 	set2 = set1
		# except:
		# 	pass

	return curvatures