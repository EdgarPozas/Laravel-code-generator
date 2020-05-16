<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class {{name}} extends Model
{
	protected $fillable=[{{fillable}}];
	protected $hidden=[{{hidden}}];
	protected $casts=[{{casts}}];
	public $timestamps = false;
{{foreign}}
}